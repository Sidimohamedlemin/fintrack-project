from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from finance.views import dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('finance/', include('finance.urls')),
    path('', dashboard, name='home'),  # ✅ Only one root URL
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
