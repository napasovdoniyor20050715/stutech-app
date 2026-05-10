from django import forms
from .models import Course, Lesson, Enrollment
from accounts.models import User

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description', 'teacher', 'category', 'level', 'duration_weeks', 'emoji', 'color', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'content', 'order', 'file', 'video_url']
        widgets = {'content': forms.Textarea(attrs={'rows': 5})}

class EnrollmentForm(forms.Form):
    student = forms.ModelChoiceField(
        queryset=User.objects.filter(role='student'),
        label='Talaba tanlang',
        empty_label='— Talabani tanlang —'
    )
