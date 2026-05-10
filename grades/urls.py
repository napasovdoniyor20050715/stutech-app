from django.urls import path
from . import views
urlpatterns = [
    path('', views.grades_overview, name='grades_overview'),
    path('course/<int:course_pk>/', views.course_grades, name='course_grades'),
]
