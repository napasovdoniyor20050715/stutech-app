from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import AttendanceSession, AttendanceRecord
from courses.models import Course, Enrollment
from accounts.models import User

@login_required
def attendance_list(request):
    if request.user.is_teacher():
        sessions = AttendanceSession.objects.filter(course__teacher=request.user)
        courses = Course.objects.filter(teacher=request.user, is_active=True)
    elif request.user.is_admin():
        sessions = AttendanceSession.objects.all()
        courses = Course.objects.filter(is_active=True)
    else:
        enrollments = request.user.enrollment_set.filter(is_active=True)
        sessions = AttendanceSession.objects.filter(course__in=[e.course for e in enrollments])
        courses = []
    return render(request, 'attendance/list.html', {'sessions': sessions[:20], 'courses': courses})

@login_required
def take_attendance(request, course_pk):
    course = get_object_or_404(Course, pk=course_pk)
    if not (request.user.is_admin() or course.teacher == request.user):
        return redirect('attendance_list')
    students = Enrollment.objects.filter(course=course, is_active=True).select_related('student')
    today = timezone.now().date()
    session, created = AttendanceSession.objects.get_or_create(
        course=course, date=today,
        defaults={'teacher': request.user}
    )
    if request.method == 'POST':
        for enrollment in students:
            student = enrollment.student
            status = request.POST.get(f'status_{student.pk}', 'absent')
            note = request.POST.get(f'note_{student.pk}', '')
            AttendanceRecord.objects.update_or_create(
                session=session, student=student,
                defaults={'status': status, 'note': note}
            )
        messages.success(request, "Davomat saqlandi!")
        return redirect('attendance_list')
    existing = {r.student_id: r for r in session.records.all()}
    return render(request, 'attendance/take.html', {
        'course': course, 'students': students, 'session': session, 'existing': existing
    })

@login_required
def student_attendance(request, student_pk=None):
    if student_pk and (request.user.is_admin() or request.user.is_teacher()):
        student = get_object_or_404(User, pk=student_pk)
    else:
        student = request.user
    records = AttendanceRecord.objects.filter(student=student).select_related('session__course').order_by('-session__date')
    total = records.count()
    present = records.filter(status='present').count()
    pct = round(present/total*100) if total else 0
    return render(request, 'attendance/student.html', {
        'student': student, 'records': records, 'total': total, 'present': present, 'pct': pct
    })

urlpatterns = []
