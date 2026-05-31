from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('boshqaruv-panel/', admin.site.urls),
    path('', include('accounts.urls')),
    path('courses/', include('courses.urls')),
    path('assignments/', include('assignments.urls')),
    path('attendance/', include('attendance.urls')),
    path('grades/', include('grades.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
