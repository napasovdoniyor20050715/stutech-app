from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ("admin", "Administrator"),
        ("teacher", "O'qituvchi"),
        ("student", "Talaba"),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="student")
    phone = models.CharField(max_length=15, blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    bio = models.TextField(blank=True)

    def is_admin(self): return self.role == "admin"
    def is_teacher(self): return self.role == "teacher"
    def is_student(self): return self.role == "student"

    def unread_notifications(self):
        return self.notifications.filter(is_read=False).count()

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"


class Notification(models.Model):
    TYPE_CHOICES = [
        ("assignment", "Yangi vazifa"),
        ("grade", "Baho qo'yildi"),
        ("submission", "Topshiriq keldi"),
        ("info", "Ma'lumot"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default="info")
    title = models.CharField(max_length=200)
    message = models.TextField()
    link = models.CharField(max_length=200, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} — {self.title}"


class LoginHistory(models.Model):
    DEVICE_CHOICES = [
        ("mobile", "📱 Mobil"),
        ("tablet", "📟 Planshet"),
        ("desktop", "🖥 Kompyuter"),
        ("unknown", "❓ Noma'lum"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="login_history")
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    device_type = models.CharField(max_length=10, choices=DEVICE_CHOICES, default="unknown")
    browser = models.CharField(max_length=100, blank=True)
    os_info = models.CharField(max_length=100, blank=True)
    login_time = models.DateTimeField(auto_now_add=True)
    is_success = models.BooleanField(default=True)

    class Meta:
        ordering = ["-login_time"]

    def __str__(self):
        return f"{self.user.username} — {self.login_time.strftime('%d.%m.%Y %H:%M')}"
