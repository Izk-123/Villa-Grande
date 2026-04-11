from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from lodge.admin_site import admin_site
from lodge.views import admin_dashboard_stats
from django.conf.urls import handler404

handler404 = 'lodge.views.custom_404'   # optional, but we'll use a simple view

urlpatterns = [
    
    # Django default admin (keep at /admin/)
    path('admin/', admin.site.urls),
    path('admin/dashboard/stats/', admin_dashboard_stats, name='admin_dashboard_stats'),
    # Custom Villa Grande Admin
    # path('admin/', admin_site.urls),
    
    # Your app URLs
    path('', include('lodge.urls')),
    path('accounts/', include('accounts.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)