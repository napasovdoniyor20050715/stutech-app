from .models import Notification

def send_notification(user, type, title, message, link=''):
    """Foydalanuvchiga bildirishnoma yuborish"""
    Notification.objects.create(
        user=user,
        type=type,
        title=title,
        message=message,
        link=link
    )

def notify_new_assignment(assignment):
    """Yangi vazifa yaratilganda barcha talabalar xabardor bo'lsin"""
    from courses.models import Enrollment
    enrollments = Enrollment.objects.filter(course=assignment.course, is_active=True)
    for enrollment in enrollments:
        send_notification(
            user=enrollment.student,
            type='assignment',
            title=f"Yangi vazifa: {assignment.title}",
            message=f"{assignment.course.name} kursida yangi vazifa qo'shildi. Muddat: {assignment.due_date.strftime('%d.%m.%Y %H:%M')}",
            link=f"/assignments/{assignment.pk}/"
        )

def notify_grade_given(submission):
    """Baho qo'yilganda talabaga xabar"""
    send_notification(
        user=submission.student,
        type='grade',
        title=f"Bahoyingiz qo'yildi!",
        message=f"{submission.assignment.title} vazifangiz tekshirildi. Bahoyingiz: {submission.score}/{submission.assignment.max_score} — {submission.grade}",
        link=f"/assignments/{submission.assignment.pk}/"
    )

def notify_new_submission(submission):
    """Talaba topshirganda o'qituvchiga xabar"""
    teacher = submission.assignment.course.teacher
    if teacher:
        send_notification(
            user=teacher,
            type='submission',
            title=f"Yangi topshiriq keldi",
            message=f"{submission.student.get_full_name() or submission.student.username} — {submission.assignment.title} vazifasini topshirdi",
            link=f"/assignments/{submission.assignment.pk}/"
        )
