from django.urls import path
from . import views

app_name = 'lodge'

handler404 = views.custom_404

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('services/', views.ServicesView.as_view(), name='services'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('rooms/', views.RoomListView.as_view(), name='rooms'),
    path('rooms/<int:pk>/', views.RoomDetailView.as_view(), name='room_detail'),
    path('rooms/available/', views.AvailableRoomsView.as_view(), name='available_rooms'),
    path('book/', views.BookingCreateView.as_view(), name='booking'),
    path('check-booking/', views.CheckBookingView.as_view(), name='check_booking'),
    path('book/success/<int:pk>/', views.BookingSuccessView.as_view(), name='booking_success'),
    path('newsletter/subscribe/', views.NewsletterSubscribeView.as_view(), name='newsletter_subscribe'),

    # Admin URLs
    path('accounts/rooms/', views.AdminRoomListView.as_view(), name='admin_room_list'),
    path('accounts/rooms/create/', views.AdminRoomCreateView.as_view(), name='admin_room_create'),
    path('accounts/rooms/<int:pk>/edit/', views.AdminRoomUpdateView.as_view(), name='admin_room_edit'),
    path('accounts/rooms/<int:pk>/delete/', views.AdminRoomDeleteView.as_view(), name='admin_room_delete'),
    path('accounts/bookings/', views.AdminBookingListView.as_view(), name='admin_booking_list'),
    path('accounts/bookings/<int:pk>/', views.AdminBookingUpdateView.as_view(), name='admin_booking_update'),
    path('accounts/customers/', views.AdminCustomerListView.as_view(), name='admin_customer_list'),
    
    # In lodge/urls.py
    path('accounts/dashboard/stats/', views.admin_dashboard_stats, name='admin_dashboard_stats'),
]
