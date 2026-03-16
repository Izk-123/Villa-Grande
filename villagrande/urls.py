from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from lodge.admin_site import admin_site

urlpatterns = [
    # Custom admin panel (using /cms/ instead of /admin/ to avoid conflict)
    path('cms/', include('lodge.admin_urls')),
    
    # Django default admin (keep at /admin/)
    # path('admin/', admin.site.urls),
    # Custom Villa Grande Admin
    path('admin/', admin_site.urls),
    
    # Your app URLs
    path('', include('lodge.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)