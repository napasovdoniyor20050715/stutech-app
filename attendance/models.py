from django.db import models
from accounts.models import User
from courses.models import Course

class AttendanceSession(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sessions')
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to={'role':'teacher'})
    date = models.DateField()
    topic = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        unique_together = ['course', 'date']

    def __str__(self): return f"{self.course.name} — {self.date}"

class AttendanceRecord(models.Model):
    STATUS = [('present','Keldi'), ('absent','Kelmadi'), ('late','Kech keldi'), ('excused','Sababli')]
    session = models.ForeignKey(AttendanceSession, on_delete=models.CASCADE, related_name='records')
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role':'student'})
    status = models.CharField(max_length=10, choices=STATUS, default='absent')
    note = models.CharField(max_length=200, blank=True)

    class Meta:
        unique_together = ['session', 'student']

    def __str__(self): return f"{self.student} — {self.session.date} — {self.status}"
