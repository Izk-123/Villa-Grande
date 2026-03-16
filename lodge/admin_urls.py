from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'cms'

urlpatterns = [
    # Authentication
    path('login/', auth_views.LoginView.as_view(
        template_name='lodge/admin/login.html',
        redirect_authenticated_user=True
    ), name='login'),
    
    path('logout/', auth_views.LogoutView.as_view(
        template_name='lodge/admin/logout.html'
    ), name='logout'),
    
    # Dashboard
    path('dashboard/', views.AdminDashboardView.as_view(), name='dashboard'),
    
    # Room Management
    path('rooms/', views.AdminRoomListView.as_view(), name='room_list'),
    path('rooms/create/', views.AdminRoomCreateView.as_view(), name='room_create'),
    path('rooms/<int:pk>/edit/', views.AdminRoomUpdateView.as_view(), name='room_edit'),
    path('rooms/<int:pk>/delete/', views.AdminRoomDeleteView.as_view(), name='room_delete'),
    
    # Booking Management
    path('bookings/', views.AdminBookingListView.as_view(), name='booking_list'),
    path('bookings/<int:pk>/', views.AdminBookingUpdateView.as_view(), name='booking_update'),
    
    # Customer Management
    path('customers/', views.AdminCustomerListView.as_view(), name='customer_list'),
]