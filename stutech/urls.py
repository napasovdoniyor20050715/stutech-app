from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from functools import wraps
from django.shortcuts import redirect

def admin_only(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_superuser:
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper

# Admin ni faqat superuser ko'ra olsin, boshqalar dashboard ga ketsin
admin.site.login = lambda request, **kwargs: redirect('/dashboard/')

urlpatterns = [
    path('boshqaruv-panel/', admin.site.urls),  # /admin/ o'rniga yashirin URL
    path('', include('accounts.urls')),
    path('courses/', include('courses.urls')),
    path('assignments/', include('assignments.urls')),
    path('attendance/', include('attendance.urls')),
    path('grades/', include('grades.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
