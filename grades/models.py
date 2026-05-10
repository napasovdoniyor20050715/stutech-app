from django.db import models
from accounts.models import User
from courses.models import Course

class Grade(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role':'student'})
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    assignment = models.ForeignKey('assignments.Assignment', on_delete=models.SET_NULL, null=True, blank=True)
    score = models.PositiveIntegerField()
    letter = models.CharField(max_length=2, blank=True)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.letter:
            self.letter = 'A' if self.score >= 90 else 'B' if self.score >= 75 else 'C' if self.score >= 60 else 'D'
        super().save(*args, **kwargs)

    def __str__(self): return f"{self.student} — {self.course} — {self.score}"
