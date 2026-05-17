from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg
from .models import User, Notification, LoginHistory
from .forms import LoginForm, UserCreateForm, UserEditForm, ProfileEditForm
from courses.models import Course, Enrollment
from assignments.models import Assignment, Submission
from attendance.models import AttendanceRecord
from grades.models import Grade

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')

def parse_user_agent(ua_string):
    ua = ua_string.lower()
    # Device
    if any(x in ua for x in ['iphone', 'android', 'mobile', 'blackberry']):
        device = 'mobile'
    elif any(x in ua for x in ['ipad', 'tablet']):
        device = 'tablet'
    elif any(x in ua for x in ['windows', 'macintosh', 'linux', 'x11']):
        device = 'desktop'
    else:
        device = 'unknown'
    # Browser
    if 'chrome' in ua and 'edg' not in ua:
        browser = 'Chrome'
    elif 'firefox' in ua:
        browser = 'Firefox'
    elif 'safari' in ua and 'chrome' not in ua:
        browser = 'Safari'
    elif 'edg' in ua:
        browser = 'Edge'
    elif 'opera' in ua or 'opr' in ua:
        browser = 'Opera'
    else:
        browser = 'Boshqa'
    # OS
    if 'windows' in ua:
        os_info = 'Windows'
    elif 'android' in ua:
        os_info = 'Android'
    elif 'iphone' in ua or 'ipad' in ua:
        os_info = 'iOS'
    elif 'macintosh' in ua:
        os_info = 'macOS'
    elif 'linux' in ua:
        os_info = 'Linux'
    else:
        os_info = "Noma'lum"
    return device, browser, os_info

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Login tarixini saqlash
            ua_string = request.META.get('HTTP_USER_AGENT', '')
            device, browser, os_info = parse_user_agent(ua_string)
            LoginHistory.objects.create(
                user=user,
                ip_address=get_client_ip(request),
                user_agent=ua_string[:500],
                device_type=device,
                browser=browser,
                os_info=os_info,
                is_success=True
            )
            messages.success(request, f"Xush kelibsiz, {user.get_full_name() or user.username}!")
            return redirect('dashboard')
        else:
            messages.error(request, "Login yoki parol noto'g'ri!")
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    user = request.user
    ctx = {}
    if user.is_admin():
        ctx['total_students'] = User.objects.filter(role='student').count()
        ctx['total_teachers'] = User.objects.filter(role='teacher').count()
        ctx['total_courses'] = Course.objects.filter(is_active=True).count()
        ctx['recent_students'] = User.objects.filter(role='student').order_by('-date_joined')[:8]
        ctx['recent_courses'] = Course.objects.order_by('-created_at')[:6]
        ctx['pending_submissions'] = Submission.objects.filter(score__isnull=True).count()
    elif user.is_teacher():
        my_courses = Course.objects.filter(teacher=user, is_active=True)
        ctx['my_courses'] = my_courses
        ctx['total_students'] = Enrollment.objects.filter(course__teacher=user).values('student').distinct().count()
        ctx['pending_submissions'] = Submission.objects.filter(assignment__course__teacher=user, score__isnull=True).count()
        ctx['total_assignments'] = Assignment.objects.filter(course__teacher=user).count()
        ctx['recent_submissions'] = Submission.objects.filter(assignment__course__teacher=user).order_by('-submitted_at')[:5]
    else:
        my_enrollments = Enrollment.objects.filter(student=user).select_related('course')
        ctx['my_enrollments'] = my_enrollments
        from django.utils import timezone
        submitted_ids = Submission.objects.filter(student=user).values_list('assignment_id', flat=True)
        ctx['pending_assignments'] = Assignment.objects.filter(
            course__enrollment__student=user,
            due_date__gte=timezone.now()
        ).exclude(id__in=submitted_ids).count()
        grades = Grade.objects.filter(student=user)
        ctx['avg_grade'] = grades.aggregate(Avg('score'))['score__avg'] or 0
        att = AttendanceRecord.objects.filter(student=user)
        total = att.count()
        present = att.filter(status='present').count()
        ctx['attendance_pct'] = round(present/total*100) if total else 0
        ctx['recent_grades'] = grades.order_by('-created_at')[:5]
    # Notifications
    ctx['notifications'] = user.notifications.filter(is_read=False)[:5]
    return render(request, 'accounts/dashboard.html', ctx)

@login_required
def users_list(request):
    if not request.user.is_admin():
        return redirect('dashboard')
    role = request.GET.get('role', '')
    q = request.GET.get('q', '')
    users = User.objects.all()
    if role:
        users = users.filter(role=role)
    if q:
        users = users.filter(first_name__icontains=q) | users.filter(last_name__icontains=q) | users.filter(username__icontains=q)
    users = users.order_by('role', 'first_name')
    return render(request, 'accounts/users_list.html', {'users': users, 'role_filter': role, 'q': q})

@login_required
def user_create(request):
    if not request.user.is_admin():
        return redirect('dashboard')
    form = UserCreateForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Foydalanuvchi muvaffaqiyatli qo'shildi!")
        return redirect('users_list')
    return render(request, 'accounts/user_form.html', {'form': form, 'title': "Yangi foydalanuvchi qo'shish"})

@login_required
def user_edit(request, pk):
    if not request.user.is_admin():
        return redirect('dashboard')
    user_obj = get_object_or_404(User, pk=pk)
    form = UserEditForm(request.POST or None, request.FILES or None, instance=user_obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f"{user_obj.get_full_name() or user_obj.username} ma'lumotlari yangilandi!")
        return redirect('users_list')
    return render(request, 'accounts/user_form.html', {
        'form': form,
        'title': f"Tahrirlash — {user_obj.get_full_name() or user_obj.username}",
        'user_obj': user_obj
    })

@login_required
def user_delete(request, pk):
    if not request.user.is_admin():
        return redirect('dashboard')
    user_obj = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        name = user_obj.get_full_name() or user_obj.username
        user_obj.delete()
        messages.success(request, f"{name} o'chirildi!")
    return redirect('users_list')

@login_required
def profile(request):
    form = ProfileEditForm(request.POST or None, request.FILES or None, instance=request.user)
    if request.method == 'POST' and form.is_valid():
        user = form.save(commit=False)
        new_pass = form.cleaned_data.get('new_password')
        if new_pass:
            user.set_password(new_pass)
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Profil va parol yangilandi! Qayta kirdingiz.")
        else:
            user.save()
            messages.success(request, "Profil yangilandi!")
        return redirect('profile')
    return render(request, 'accounts/profile.html', {'form': form})

@login_required
def notifications_list(request):
    notifs = request.user.notifications.all()
    # Mark all as read
    notifs.filter(is_read=False).update(is_read=True)
    return render(request, 'accounts/notifications.html', {'notifications': notifs})

@login_required
def notification_read(request, pk):
    notif = get_object_or_404(Notification, pk=pk, user=request.user)
    notif.is_read = True
    notif.save()
    if notif.link:
        return redirect(notif.link)
    return redirect('notifications_list')

@login_required
def login_history(request):
    if not request.user.is_admin():
        return redirect('dashboard')
    histories = LoginHistory.objects.select_related('user').all()[:200]
    return render(request, 'accounts/login_history.html', {'histories': histories})
