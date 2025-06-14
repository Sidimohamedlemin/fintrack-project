from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from finance.views import dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('finance/', include('finance.urls')),
    path('users/', include('users.urls')),  
    path('', dashboard, name='home'),
    path('about/', TemplateView.as_view(template_name="about.html"), name='about'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# Serve media files during development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
