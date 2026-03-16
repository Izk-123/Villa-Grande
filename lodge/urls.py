from django.urls import path
from . import views

app_name = 'lodge'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('services/', views.ServicesView.as_view(), name='services'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('rooms/', views.RoomListView.as_view(), name='rooms'),
    path('rooms/<int:pk>/', views.RoomDetailView.as_view(), name='room_detail'),
    path('book/', views.BookingCreateView.as_view(), name='booking'),
    path('book/success/<int:pk>/', views.BookingSuccessView.as_view(), name='booking_success'),

    # Admin URLs
    path('admin/dashboard/', views.AdminDashboardView.as_view(), name='admin_dashboard'),
    path('admin/rooms/', views.AdminRoomListView.as_view(), name='admin_room_list'),
    path('admin/rooms/create/', views.AdminRoomCreateView.as_view(), name='admin_room_create'),
    path('admin/rooms/<int:pk>/edit/', views.AdminRoomUpdateView.as_view(), name='admin_room_edit'),
    path('admin/rooms/<int:pk>/delete/', views.AdminRoomDeleteView.as_view(), name='admin_room_delete'),
    path('admin/bookings/', views.AdminBookingListView.as_view(), name='admin_booking_list'),
    path('admin/bookings/<int:pk>/', views.AdminBookingUpdateView.as_view(), name='admin_booking_update'),
    path('admin/customers/', views.AdminCustomerListView.as_view(), name='admin_customer_list'),
]