"""
StuTech - Demo ma'lumotlar yaratish skripti
Ishlatish: python seed_data.py
"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stutech.settings')
django.setup()

from accounts.models import User
from courses.models import Course, Enrollment
from assignments.models import Assignment, Submission
from grades.models import Grade
from django.utils import timezone
from datetime import timedelta

print("🚀 Demo ma'lumotlar yaratilmoqda...")

# Admin — parolni FAQAT yangi yaratilganda o'rnatamiz
admin, created = User.objects.get_or_create(username='admin', defaults={
    'first_name': 'Jamshid', 'last_name': 'Abdullayev',
    'email': 'admin@stutech.uz', 'role': 'admin', 'is_staff': True, 'is_superuser': True
})
if created:
    admin.set_password('admin123')
    admin.save()
    print("✓ Admin yaratildi: admin / admin123")
else:
    print("✓ Admin allaqachon mavjud — paroli o'zgartirilmadi")

# Teachers — parolni faqat yangi yaratilganda
t1, created = User.objects.get_or_create(username='teacher', defaults={
    'first_name': 'Ulugbek', 'last_name': 'Nazarov',
    'email': 'teacher@stutech.uz', 'role': 'teacher'
})
if created:
    t1.set_password('teacher123')
    t1.save()

t2, created = User.objects.get_or_create(username='teacher2', defaults={
    'first_name': 'Diana', 'last_name': 'Ismoilova',
    'email': 'diana@stutech.uz', 'role': 'teacher'
})
if created:
    t2.set_password('teacher123')
    t2.save()

t3, created = User.objects.get_or_create(username='teacher3', defaults={
    'first_name': 'Farrux', 'last_name': 'Sobirov',
    'email': 'farrux@stutech.uz', 'role': 'teacher'
})
if created:
    t3.set_password('teacher123')
    t3.save()

print("✓ O'qituvchilar tekshirildi")

# Students — faqat yangilari qo'shiladi
students = []
student_data = [
    ('student', 'Sardor', 'Karimov'),
    ('student2', 'Nilufar', 'Toshmatova'),
    ('student3', 'Bobur', 'Xasanov'),
    ('student4', 'Malika', 'Yusupova'),
    ('student5', 'Jasur', 'Rahimov'),
    ('student6', 'Zulfiya', 'Mirzayeva'),
    ('student7', 'Sherzod', 'Ergashev'),
    ('student8', 'Mohira', 'Qodirov'),
]
for uname, fname, lname in student_data:
    s, created = User.objects.get_or_create(username=uname, defaults={
        'first_name': fname, 'last_name': lname,
        'email': f'{uname}@stutech.uz', 'role': 'student'
    })
    if created:
        s.set_password('student123')
        s.save()
    students.append(s)

print(f"✓ Talabalar tekshirildi")

# Courses
courses_data = [
    ('Python dasturlash', 'programming', 'beginner', '🐍', 'blue', t1, 'Python dasturlash tilini noldan o\'rganish.'),
    ('Django Framework', 'programming', 'intermediate', '🌐', 'teal', t1, 'Django web framework yordamida real ilovalar yaratish.'),
    ('UI/UX Dizayn', 'design', 'beginner', '🎨', 'purple', t3, 'Foydalanuvchi interfeysi va tajribasini loyihalash.'),
    ('Grafik dizayn', 'design', 'beginner', '✏️', 'pink', t3, 'Adobe Photoshop va Illustrator bilan ishlash.'),
    ('Ingliz tili A2-B1', 'languages', 'beginner', '🇬🇧', 'amber', t2, 'Ingliz tilini A2 darajasidan B1 gacha.'),
    ('Ingliz tili B2', 'languages', 'intermediate', '🗣️', 'green', t2, 'Yuqori darajadagi ingliz tili.'),
    ('Matematika (asosiy)', 'math', 'beginner', '📐', 'blue', admin, 'Maktab matematikasini chuqurlashtirish.'),
    ('Algebra va Analiz', 'math', 'advanced', '∞', 'purple', admin, 'Oliy matematika kursi.'),
    ('Flutter Mobile', 'programming', 'intermediate', '📱', 'teal', t1, 'Flutter yordamida mobil ilovalar yaratish.'),
    ('SQL va PostgreSQL', 'programming', 'beginner', '🗄️', 'amber', t1, 'Ma\'lumotlar bazasi asoslari.'),
    ('Kompyuter savodxonligi', 'other', 'beginner', '💻', 'blue', admin, 'MS Office, Internet asoslari.'),
    ('Fizika', 'science', 'beginner', '⚛️', 'red', admin, 'Umumiy fizika kursi.'),
]

created_courses = []
for name, cat, level, emoji, color, teacher, desc in courses_data:
    c, _ = Course.objects.get_or_create(name=name, defaults={
        'category': cat, 'level': level, 'emoji': emoji,
        'color': color, 'teacher': teacher, 'description': desc,
        'duration_weeks': 8, 'is_active': True
    })
    created_courses.append(c)

print(f"✓ Kurslar tekshirildi")

# Enrollments
enrollments = [
    (students[0], [0, 1, 4]),
    (students[1], [0, 2, 4]),
    (students[2], [0, 1, 6]),
    (students[3], [2, 4, 5]),
    (students[4], [3, 4, 7]),
    (students[5], [4, 5, 6]),
    (students[6], [0, 8, 9]),
    (students[7], [2, 3, 10]),
]
for student, course_indices in enrollments:
    for idx in course_indices:
        Enrollment.objects.get_or_create(student=student, course=created_courses[idx])

print("✓ Yozilishlar tekshirildi")

print("\n🎉 Hammasi tayyor!")
print("━" * 40)
print("Login ma'lumotlari:")
print("  Admin:       admin / (o'zgartirilgan parol)")
print("  O'qituvchi:  teacher / teacher123")
print("  Talaba:      student / student123")
print("━" * 40)
