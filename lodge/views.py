from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils import timezone

from .models import Room, Booking, Customer
from .forms import BookingForm, RoomForm   # ✅ Import RoomForm here


# ---------- WhatsApp Notification Helpers (Simulated) ----------
def send_whatsapp_notification(booking):
    """Simulate sending a WhatsApp message for a new booking."""
    print(f"WhatsApp message to {booking.customer.phone}:")
    print(f"Booking {booking.id} for {booking.room} from {booking.check_in} to {booking.check_out} is pending.")


def send_whatsapp_confirmation(booking):
    """Simulate sending a WhatsApp confirmation when booking is confirmed."""
    print(f"WhatsApp confirmation to {booking.customer.phone}:")
    print(f"Your booking at Villa Grande is confirmed! Booking ID: {booking.id}")


# ---------- Customer Facing Views ----------
class HomeView(TemplateView):
    template_name = 'lodge/index.html'
    
class AboutView(TemplateView):
    template_name = 'lodge/about.html'

class ServicesView(TemplateView):
    template_name = 'lodge/services.html'

class ContactView(TemplateView):
    template_name = 'lodge/contact.html'

class RoomListView(ListView):
    model = Room
    template_name = 'lodge/rooms.html'
    context_object_name = 'rooms'
    queryset = Room.objects.filter(is_active=True)


class RoomDetailView(DetailView):
    model = Room
    template_name = 'lodge/room_detail.html'
    context_object_name = 'room'


class BookingCreateView(View):
    def get(self, request):
        form = BookingForm()
        # Pre‑select room if passed in query string
        room_id = request.GET.get('room')
        if room_id:
            try:
                room = Room.objects.get(pk=room_id, is_active=True)
                form.fields['room'].initial = room
            except Room.DoesNotExist:
                pass
        return render(request, 'lodge/booking.html', {'form': form})

    def post(self, request):
        form = BookingForm(request.POST)
        if form.is_valid():
            # Get or create customer
            customer, created = Customer.objects.get_or_create(
                phone=form.cleaned_data['phone'],
                defaults={
                    'name': form.cleaned_data['name'],
                    'email': form.cleaned_data.get('email', '')
                }
            )
            # Create booking
            booking = Booking.objects.create(
                customer=customer,
                room=form.cleaned_data['room'],
                check_in=form.cleaned_data['check_in'],
                check_out=form.cleaned_data['check_out'],
                guests=form.cleaned_data['guests'],
                status='PENDING'
            )
            send_whatsapp_notification(booking)
            messages.success(request, 'Booking request submitted! We will confirm shortly.')
            return redirect('lodge:booking_success', pk=booking.pk)
        return render(request, 'lodge/booking.html', {'form': form})


class BookingSuccessView(TemplateView):
    template_name = 'lodge/booking_success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['booking'] = get_object_or_404(Booking, pk=self.kwargs['pk'])
        return context


# ---------- Admin Views (Login Required) ----------
class AdminDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'lodge/admin/dashboard.html'
    login_url = '/admin/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_rooms'] = Room.objects.count()
        context['active_rooms'] = Room.objects.filter(is_active=True).count()
        context['pending_bookings'] = Booking.objects.filter(status='PENDING').count()
        context['confirmed_bookings'] = Booking.objects.filter(status='CONFIRMED').count()
        context['today_bookings'] = Booking.objects.filter(check_in=timezone.now().date()).count()
        return context


class AdminRoomListView(LoginRequiredMixin, ListView):
    model = Room
    template_name = 'lodge/admin/room_list.html'
    context_object_name = 'rooms'
    login_url = '/admin/login/'


class AdminRoomCreateView(LoginRequiredMixin, CreateView):
    model = Room
    form_class = RoomForm
    template_name = 'lodge/admin/room_form.html'
    success_url = reverse_lazy('lodge:admin_room_list')
    login_url = '/admin/login/'


class AdminRoomUpdateView(LoginRequiredMixin, UpdateView):
    model = Room
    form_class = RoomForm
    template_name = 'lodge/admin/room_form.html'
    success_url = reverse_lazy('lodge:admin_room_list')
    login_url = '/admin/login/'


class AdminRoomDeleteView(LoginRequiredMixin, DeleteView):
    model = Room
    template_name = 'lodge/admin/room_confirm_delete.html'
    success_url = reverse_lazy('lodge:admin_room_list')
    login_url = '/admin/login/'


class AdminBookingListView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'lodge/admin/booking_list.html'
    context_object_name = 'bookings'
    login_url = '/admin/login/'
    ordering = ['-created_at']

    def get_queryset(self):
        return Booking.objects.select_related('customer', 'room').all()


class AdminBookingUpdateView(LoginRequiredMixin, UpdateView):
    model = Booking
    fields = ['status']
    template_name = 'lodge/admin/booking_form.html'
    success_url = reverse_lazy('lodge:admin_booking_list')
    login_url = '/admin/login/'

    def form_valid(self, form):
        response = super().form_valid(form)
        if form.instance.status == 'CONFIRMED':
            send_whatsapp_confirmation(form.instance)
        return response


class AdminCustomerListView(LoginRequiredMixin, ListView):
    model = Customer
    template_name = 'lodge/admin/customer_list.html'
    context_object_name = 'customers'
    login_url = '/admin/login/'
    paginate_by = 20