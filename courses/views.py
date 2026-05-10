from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course, Lesson, Enrollment
from .forms import CourseForm, LessonForm, EnrollmentForm
from accounts.models import User

@login_required
def course_list(request):
    cat = request.GET.get('cat', '')
    q = request.GET.get('q', '')
    courses = Course.objects.filter(is_active=True)
    if request.user.is_teacher():
        courses = courses.filter(teacher=request.user)
    if cat:
        courses = courses.filter(category=cat)
    if q:
        courses = courses.filter(name__icontains=q)
    enrolled_ids = []
    if request.user.is_student():
        enrolled_ids = list(Enrollment.objects.filter(student=request.user).values_list('course_id', flat=True))
    return render(request, 'courses/list.html', {
        'courses': courses, 'cat_filter': cat, 'q': q, 'enrolled_ids': enrolled_ids
    })

@login_required
def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    lessons = course.lessons.all()
    is_enrolled = False
    if request.user.is_student():
        is_enrolled = Enrollment.objects.filter(student=request.user, course=course).exists()
    students = Enrollment.objects.filter(course=course, is_active=True).select_related('student')
    return render(request, 'courses/detail.html', {
        'course': course, 'lessons': lessons, 'is_enrolled': is_enrolled, 'students': students
    })

@login_required
def course_create(request):
    if not (request.user.is_admin() or request.user.is_teacher()):
        return redirect('course_list')
    form = CourseForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        course = form.save(commit=False)
        if request.user.is_teacher():
            course.teacher = request.user
        course.save()
        messages.success(request, "Kurs muvaffaqiyatli yaratildi!")
        return redirect('course_detail', pk=course.pk)
    return render(request, 'courses/form.html', {'form': form, 'title': 'Yangi kurs'})

@login_required
def course_edit(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if not (request.user.is_admin() or course.teacher == request.user):
        return redirect('course_list')
    form = CourseForm(request.POST or None, instance=course)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Kurs yangilandi!")
        return redirect('course_detail', pk=course.pk)
    return render(request, 'courses/form.html', {'form': form, 'title': 'Kursni tahrirlash', 'course': course})

@login_required
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.user.is_admin() and request.method == 'POST':
        course.delete()
        messages.success(request, "O'chirildi!")
    return redirect('course_list')

@login_required
def lesson_create(request, course_pk):
    course = get_object_or_404(Course, pk=course_pk)
    if not (request.user.is_admin() or course.teacher == request.user):
        return redirect('course_detail', pk=course_pk)
    form = LessonForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        lesson = form.save(commit=False)
        lesson.course = course
        lesson.save()
        messages.success(request, "Dars qo'shildi!")
        return redirect('course_detail', pk=course_pk)
    return render(request, 'courses/lesson_form.html', {'form': form, 'course': course})

@login_required
def enroll_student(request, course_pk):
    course = get_object_or_404(Course, pk=course_pk)
    if not (request.user.is_admin() or course.teacher == request.user):
        return redirect('course_detail', pk=course_pk)
    form = EnrollmentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        student = form.cleaned_data['student']
        _, created = Enrollment.objects.get_or_create(student=student, course=course)
        if created:
            messages.success(request, f"{student.get_full_name()} kursga qo'shildi!")
        else:
            messages.warning(request, "Bu talaba allaqachon yozilgan!")
        return redirect('course_detail', pk=course_pk)
    return render(request, 'courses/enroll_form.html', {'form': form, 'course': course})
