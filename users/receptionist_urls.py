from django.urls import path
from . import views

app_name = 'receptionist'

urlpatterns = [
    path('', views.ReceptionistDashboardView.as_view(), name='dashboard'),
    path('bookings/', views.ReceptionistBookingListView.as_view(), name='booking_list'),
    path('bookings/create/', views.ReceptionistBookingCreateView.as_view(), name='booking_create'),
    path('bookings/<int:pk>/edit/', views.ReceptionistBookingUpdateView.as_view(), name='booking_edit'),
    path('customers/', views.ReceptionistCustomerListView.as_view(), name='customer_list'),
    path('customers/create/', views.ReceptionistCustomerCreateView.as_view(), name='customer_create'),
    path('check-in/<int:pk>/', views.ReceptionistCheckInView.as_view(), name='check_in'),
    path('check-out/<int:pk>/', views.ReceptionistCheckOutView.as_view(), name='check_out'),
]