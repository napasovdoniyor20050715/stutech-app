from django.db import models
from accounts.models import User

CATEGORY_CHOICES = [
    ('programming', 'Dasturlash'),
    ('design', 'Dizayn'),
    ('languages', 'Tillar'),
    ('math', 'Matematika'),
    ('science', 'Fan'),
    ('business', 'Biznes'),
    ('other', 'Boshqa'),
]

class Course(models.Model):
    LEVEL_CHOICES = [('beginner','Boshlang\'ich'), ('intermediate','O\'rta'), ('advanced','Yuqori')]
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='courses', limit_choices_to={'role':'teacher'})
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    level = models.CharField(max_length=15, choices=LEVEL_CHOICES, default='beginner')
    duration_weeks = models.PositiveIntegerField(default=8)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    emoji = models.CharField(max_length=5, default='📚')
    color = models.CharField(max_length=20, default='blue')

    class Meta:
        ordering = ['-created_at']

    def __str__(self): return self.name

    def enrolled_count(self):
        return self.enrollment_set.filter(is_active=True).count()

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            import uuid
            self.slug = slugify(self.name) + '-' + str(uuid.uuid4())[:6]
        super().save(*args, **kwargs)

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    file = models.FileField(upload_to='lessons/', blank=True, null=True)
    video_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self): return f"{self.course.name} — {self.title}"

class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role':'student'})
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ['student', 'course']

    def __str__(self): return f"{self.student} → {self.course}"
