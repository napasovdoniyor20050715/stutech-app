from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('create/', views.course_create, name='course_create'),
    path('<int:pk>/', views.course_detail, name='course_detail'),
    path('<int:pk>/edit/', views.course_edit, name='course_edit'),
    path('<int:pk>/delete/', views.course_delete, name='course_delete'),
    path('<int:course_pk>/lessons/add/', views.lesson_create, name='lesson_create'),
    path('<int:course_pk>/enroll/', views.enroll_student, name='enroll_student'),
]
