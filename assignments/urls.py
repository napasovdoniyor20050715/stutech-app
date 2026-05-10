from django.urls import path
from . import views

urlpatterns = [
    path('', views.assignment_list, name='assignment_list'),
    path('<int:pk>/', views.assignment_detail, name='assignment_detail'),
    path('<int:pk>/submit/', views.submit_assignment, name='submit_assignment'),
    path('<int:pk>/grade/', views.grade_submission, name='grade_submission'),
    path('course/<int:course_pk>/create/', views.assignment_create, name='assignment_create'),
]
