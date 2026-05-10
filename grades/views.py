from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from .models import Grade
from courses.models import Course, Enrollment
from accounts.models import User

@login_required
def grades_overview(request):
    user = request.user
    if user.is_student():
        grades = Grade.objects.filter(student=user).select_related('course', 'assignment')
        avg = grades.aggregate(Avg('score'))['score__avg'] or 0
        by_course = {}
        for g in grades:
            by_course.setdefault(g.course, []).append(g)
        return render(request, 'grades/student_grades.html', {
            'grades': grades, 'avg': round(avg, 1), 'by_course': by_course
        })
    elif user.is_teacher():
        courses = Course.objects.filter(teacher=user, is_active=True)
        return render(request, 'grades/teacher_grades.html', {'courses': courses})
    else:
        courses = Course.objects.filter(is_active=True)
        return render(request, 'grades/teacher_grades.html', {'courses': courses})

@login_required
def course_grades(request, course_pk):
    course = get_object_or_404(Course, pk=course_pk)
    enrollments = Enrollment.objects.filter(course=course, is_active=True).select_related('student')
    data = []
    for e in enrollments:
        grades = Grade.objects.filter(student=e.student, course=course)
        avg = grades.aggregate(Avg('score'))['score__avg'] or 0
        data.append({'student': e.student, 'grades': grades, 'avg': round(avg, 1)})
    data.sort(key=lambda x: x['avg'], reverse=True)
    return render(request, 'grades/course_grades.html', {'course': course, 'data': data})
