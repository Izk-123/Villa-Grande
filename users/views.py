from django.shortcuts import render

# Create your views here.
from django.utils import timezone
from django.views.generic import TemplateView, ListView, UpdateView, CreateView
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from .decorators import receptionist_required
from lodge.models import Room, Booking, Customer

@method_decorator(receptionist_required, name='dispatch')
class ReceptionistDashboardView(TemplateView):
    template_name = 'lodge/receptionist/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        context['today_bookings'] = Booking.objects.filter(check_in=today).count()
        context['checked_in_guests'] = Booking.objects.filter(check_in=today, status='CONFIRMED').count()
        context['available_rooms'] = Room.objects.filter(is_active=True).exclude(
            bookings__check_in__lte=today, bookings__check_out__gt=today
        ).count()
        context['rooms'] = Room.objects.all()
        context['today_bookings_list'] = Booking.objects.filter(check_in=today).select_related('customer', 'room')
        return context

@method_decorator(receptionist_required, name='dispatch')
class ReceptionistBookingListView(ListView):
    model = Booking
    template_name = 'lodge/receptionist/booking_list.html'
    context_object_name = 'bookings'
    ordering = ['-created_at']

    def get_queryset(self):
        return super().get_queryset().select_related('customer', 'room')

@method_decorator(receptionist_required, name='dispatch')
class ReceptionistBookingCreateView(CreateView):
    model = Booking
    fields = ['customer', 'room', 'check_in', 'check_out', 'guests']
    template_name = 'lodge/receptionist/booking_form.html'
    success_url = reverse_lazy('receptionist:booking_list')

    def form_valid(self, form):
        form.instance.status = 'PENDING'
        response = super().form_valid(form)
        # Optional: send_whatsapp_notification(form.instance)
        messages.success(self.request, f"Booking {form.instance.id} created.")
        return response

@method_decorator(receptionist_required, name='dispatch')
class ReceptionistBookingUpdateView(UpdateView):
    model = Booking
    fields = ['status', 'room', 'check_in', 'check_out', 'guests']
    template_name = 'lodge/receptionist/booking_form.html'
    success_url = reverse_lazy('receptionist:booking_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        if form.instance.status == 'CONFIRMED':
            # Optional: send_whatsapp_confirmation(form.instance)
            pass
        messages.success(self.request, f"Booking {form.instance.id} updated.")
        return response

@method_decorator(receptionist_required, name='dispatch')
class ReceptionistCustomerListView(ListView):
    model = Customer
    template_name = 'lodge/receptionist/customer_list.html'
    context_object_name = 'customers'
    paginate_by = 20

@method_decorator(receptionist_required, name='dispatch')
class ReceptionistCustomerCreateView(CreateView):
    model = Customer
    fields = ['name', 'phone', 'email']
    template_name = 'lodge/receptionist/customer_form.html'
    success_url = reverse_lazy('receptionist:customer_list')

    def form_valid(self, form):
        messages.success(self.request, "Customer added.")
        return super().form_valid(form)

@method_decorator(receptionist_required, name='dispatch')
class ReceptionistCheckInView(UpdateView):
    model = Booking
    fields = []
    template_name = 'lodge/receptionist/check_in.html'
    success_url = reverse_lazy('receptionist:dashboard')

    def form_valid(self, form):
        booking = self.object
        booking.status = 'CONFIRMED'
        booking.save()
        messages.success(self.request, f"Checked in booking {booking.id}.")
        return super().form_valid(form)

@method_decorator(receptionist_required, name='dispatch')
class ReceptionistCheckOutView(UpdateView):
    model = Booking
    fields = []
    template_name = 'lodge/receptionist/check_out.html'
    success_url = reverse_lazy('receptionist:dashboard')

    def form_valid(self, form):
        booking = self.object
        messages.success(self.request, f"Checked out booking {booking.id}.")
        return super().form_valid(form)