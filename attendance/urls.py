from django.urls import path
from . import views

urlpatterns = [
    path('', views.attendance_list, name='attendance_list'),
    path('course/<int:course_pk>/take/', views.take_attendance, name='take_attendance'),
    path('student/', views.student_attendance, name='my_attendance'),
    path('student/<int:student_pk>/', views.student_attendance, name='student_attendance'),
]
