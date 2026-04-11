from django.urls import path, include

urlpatterns = [
    path('receptionist/', include('lodge.receptionist_urls')),
]