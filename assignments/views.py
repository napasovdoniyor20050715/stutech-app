from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Assignment, Submission
from .forms import AssignmentForm, SubmissionForm, GradeForm
from courses.models import Course, Enrollment

@login_required
def assignment_list(request):
    user = request.user
    if user.is_teacher():
        assignments = Assignment.objects.filter(course__teacher=user)
    elif user.is_student():
        enrolled = Enrollment.objects.filter(student=user).values_list('course_id', flat=True)
        assignments = Assignment.objects.filter(course_id__in=enrolled)
    else:
        assignments = Assignment.objects.all()
    submitted_ids = []
    if user.is_student():
        submitted_ids = list(Submission.objects.filter(student=user).values_list('assignment_id', flat=True))
    return render(request, 'assignments/list.html', {
        'assignments': assignments, 'submitted_ids': submitted_ids, 'now': timezone.now()
    })

@login_required
def assignment_create(request, course_pk):
    course = get_object_or_404(Course, pk=course_pk)
    if not (request.user.is_admin() or course.teacher == request.user):
        return redirect('assignment_list')
    form = AssignmentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        a = form.save(commit=False)
        a.course = course
        a.save()
        # Bildirishnoma yuborish
        from accounts.utils import notify_new_assignment
        notify_new_assignment(a)
        messages.success(request, "Vazifa yaratildi va talabalar xabardor qilindi!")
        return redirect('course_detail', pk=course_pk)
    return render(request, 'assignments/form.html', {'form': form, 'course': course})

@login_required
def assignment_detail(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    submission = None
    submissions = None
    if request.user.is_student():
        submission = Submission.objects.filter(assignment=assignment, student=request.user).first()
    else:
        submissions = assignment.submissions.select_related('student').all()
    return render(request, 'assignments/detail.html', {
        'assignment': assignment, 'submission': submission, 'submissions': submissions
    })

@login_required
def submit_assignment(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    if not request.user.is_student():
        return redirect('assignment_list')
    existing = Submission.objects.filter(assignment=assignment, student=request.user).first()
    if existing:
        messages.warning(request, "Siz allaqachon topshirdingiz!")
        return redirect('assignment_detail', pk=pk)
    form = SubmissionForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        sub = form.save(commit=False)
        sub.assignment = assignment
        sub.student = request.user
        sub.save()
        # O'qituvchiga bildirishnoma
        from accounts.utils import notify_new_submission
        notify_new_submission(sub)
        messages.success(request, "Vazifa muvaffaqiyatli topshirildi!")
        return redirect('assignment_list')
    return render(request, 'assignments/submit.html', {'form': form, 'assignment': assignment})

@login_required
def grade_submission(request, pk):
    submission = get_object_or_404(Submission, pk=pk)
    if not (request.user.is_admin() or submission.assignment.course.teacher == request.user):
        return redirect('assignment_list')
    form = GradeForm(request.POST or None, instance=submission)
    if request.method == 'POST' and form.is_valid():
        sub = form.save(commit=False)
        score = sub.score
        max_s = sub.assignment.max_score
        pct = (score / max_s * 100) if max_s else 0
        sub.grade = 'A' if pct >= 90 else 'B' if pct >= 75 else 'C' if pct >= 60 else 'D'
        sub.save()
        from grades.models import Grade
        Grade.objects.update_or_create(
            student=sub.student, course=sub.assignment.course,
            assignment=sub.assignment,
            defaults={'score': score}
        )
        # Talabaga bildirishnoma
        from accounts.utils import notify_grade_given
        notify_grade_given(sub)
        messages.success(request, "Baho qo'yildi va talaba xabardor qilindi!")
        return redirect('assignment_detail', pk=submission.assignment.pk)
    return render(request, 'assignments/grade.html', {'form': form, 'submission': submission})
