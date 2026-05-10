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

# Admin
admin, _ = User.objects.get_or_create(username='admin', defaults={
    'first_name': 'Jamshid', 'last_name': 'Abdullayev',
    'email': 'admin@stutech.uz', 'role': 'admin', 'is_staff': True, 'is_superuser': True
})
admin.set_password('admin123')
admin.save()
print("✓ Admin yaratildi: admin / admin123")

# Teachers
t1, _ = User.objects.get_or_create(username='teacher', defaults={
    'first_name': 'Ulugbek', 'last_name': 'Nazarov',
    'email': 'teacher@stutech.uz', 'role': 'teacher'
})
t1.set_password('teacher123')
t1.save()

t2, _ = User.objects.get_or_create(username='teacher2', defaults={
    'first_name': 'Diana', 'last_name': 'Ismoilova',
    'email': 'diana@stutech.uz', 'role': 'teacher'
})
t2.set_password('teacher123')
t2.save()

t3, _ = User.objects.get_or_create(username='teacher3', defaults={
    'first_name': 'Farrux', 'last_name': 'Sobirov',
    'email': 'farrux@stutech.uz', 'role': 'teacher'
})
t3.set_password('teacher123')
t3.save()
print("✓ O'qituvchilar yaratildi")

# Students
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
    s, _ = User.objects.get_or_create(username=uname, defaults={
        'first_name': fname, 'last_name': lname,
        'email': f'{uname}@stutech.uz', 'role': 'student'
    })
    s.set_password('student123')
    s.save()
    students.append(s)
print(f"✓ {len(students)} ta talaba yaratildi")

# Courses
courses_data = [
    ('Python dasturlash', 'programming', 'beginner', '🐍', 'blue', t1, 'Python dasturlash tilini noldan o\'rganish. Asosiy tushunchalar, funksiyalar, OOP.'),
    ('Django Framework', 'programming', 'intermediate', '🌐', 'teal', t1, 'Django web framework yordamida real ilovalar yaratish.'),
    ('UI/UX Dizayn', 'design', 'beginner', '🎨', 'purple', t3, 'Foydalanuvchi interfeysi va tajribasini loyihalash asoslari.'),
    ('Grafik dizayn', 'design', 'beginner', '✏️', 'pink', t3, 'Adobe Photoshop va Illustrator bilan ishlash.'),
    ('Ingliz tili A2-B1', 'languages', 'beginner', '🇬🇧', 'amber', t2, 'Ingliz tilini A2 darajasidan B1 gacha o\'rganish.'),
    ('Ingliz tili B2', 'languages', 'intermediate', '🗣️', 'green', t2, 'Yuqori darajadagi ingliz tili — suhbat va yozuv.'),
    ('Matematika (asosiy)', 'math', 'beginner', '📐', 'blue', admin, 'Maktab matematikasini chuqurlashtirish. Algebra, geometriya.'),
    ('Algebra va Analiz', 'math', 'advanced', '∞', 'purple', admin, 'Oliy matematika: chiziqli algebra, matematik analiz.'),
    ('Flutter Mobile', 'programming', 'intermediate', '📱', 'teal', t1, 'Flutter yordamida Android va iOS ilovalar yaratish.'),
    ('SQL va PostgreSQL', 'programming', 'beginner', '🗄️', 'amber', t1, 'Ma\'lumotlar bazasi asoslari, SQL so\'rovlari.'),
    ('Kompyuter savodxonligi', 'other', 'beginner', '💻', 'blue', admin, 'MS Office, Internet, asosiy kompyuter bilimlari.'),
    ('Fizika', 'science', 'beginner', '⚛️', 'red', admin, 'Umumiy fizika kursi: mexanika, optika, elektr.'),
]

created_courses = []
for name, cat, level, emoji, color, teacher, desc in courses_data:
    c, _ = Course.objects.get_or_create(name=name, defaults={
        'category': cat, 'level': level, 'emoji': emoji,
        'color': color, 'teacher': teacher, 'description': desc,
        'duration_weeks': 8, 'is_active': True
    })
    created_courses.append(c)

print(f"✓ {len(created_courses)} ta kurs yaratildi")

# Enroll students
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
print("✓ Talabalar kurslarga yozildi")

# Assignments
now = timezone.now()
for course in created_courses[:4]:
    a1, _ = Assignment.objects.get_or_create(
        course=course, title=f'{course.name} — 1-vazifa',
        defaults={'description': 'Birinchi mustaqil ish. Ko\'rsatmalarga rioya qiling.', 'due_date': now + timedelta(days=7), 'max_score': 100}
    )
    a2, _ = Assignment.objects.get_or_create(
        course=course, title=f'{course.name} — 2-vazifa',
        defaults={'description': 'Ikkinchi mustaqil ish.', 'due_date': now - timedelta(days=3), 'max_score': 100}
    )

# Sample grades
enrolled = Enrollment.objects.all()
for e in enrolled[:12]:
    asgns = Assignment.objects.filter(course=e.course, due_date__lt=now)
    for a in asgns:
        score = 70 + (hash(f"{e.student.pk}{a.pk}") % 30)
        Grade.objects.get_or_create(
            student=e.student, course=e.course, assignment=a,
            defaults={'score': abs(score)}
        )

print("✓ Vazifalar va baholar yaratildi")
print("\n🎉 Hammasi tayyor!")
print("━" * 40)
print("Login ma'lumotlari:")
print("  Admin:       admin / admin123")
print("  O'qituvchi:  teacher / teacher123")
print("  Talaba:      student / student123")
print("━" * 40)
