from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from datetime import timedelta
from django.db.models import Count
from django.utils.dateparse import parse_date
from django.db.models import Q
from django.shortcuts import redirect
from django.db import transaction
from .models import (
    Room, Booking, Customer,
    HeroSlide, AboutSection, Service,
    ExperienceSection, Testimonial, NewsletterSection, NewsletterSubscriber, SiteSettings
)
from .forms import BookingStatusForm, ModernBookingForm, RoomForm, QuickBookingForm, NewsletterForm, ContactForm  # Updated import


# ---------- WhatsApp Notification Helpers (Simulated) ----------
def send_whatsapp_notification(booking):
    print(f"WhatsApp message to {booking.customer.phone}:")
    print(f"Booking {booking.id} for {booking.room} from {booking.check_in} to {booking.check_out} is pending.")


def send_whatsapp_confirmation(booking):
    print(f"WhatsApp confirmation to {booking.customer.phone}:")
    print(f"Your booking at Villa Grande is confirmed! Booking ID: {booking.id}")


# ---------- Customer Facing Views ----------

class HomeView(TemplateView):
    template_name = 'lodge/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Hero Slides
        context['hero_slides'] = HeroSlide.objects.filter(is_active=True)
        context['today'] = timezone.now().date().isoformat()

        # About Section with statistics
        about = AboutSection.objects.filter(is_active=True).first()
        context['about'] = about
        context['statistics'] = about.statistics.all() if about else []

        # Featured Rooms
        context['featured_rooms'] = Room.objects.filter(is_active=True)[:3]

        # Services
        context['services'] = Service.objects.filter(is_active=True)[:6]

        # Experience Section
        context['experience'] = ExperienceSection.objects.filter(is_active=True).first()

        # Testimonials
        context['testimonials'] = Testimonial.objects.filter(is_active=True)[:3]

        # Newsletter Section
        context['newsletter'] = NewsletterSection.objects.filter(is_active=True).first()
        
        # Quick Booking Form
        context['quick_booking_form'] = QuickBookingForm()

        return context


# --- Updated views in views.py ---

class AboutView(TemplateView):
    template_name = 'lodge/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the active AboutSection (assuming only one is active)
        about_section = AboutSection.objects.filter(is_active=True).first()
        context['about'] = about_section
        # Get related statistics for the about section
        if about_section:
            context['statistics'] = about_section.statistics.all()
        else:
            context['statistics'] = []
        return context


class ServicesView(TemplateView):
    template_name = 'lodge/services.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get all active services, ordered by the 'order' field
        context['services'] = Service.objects.filter(is_active=True).order_by('order')
        return context

class ContactView(View):
    template_name = 'lodge/contact.html'

    def get(self, request):
        form = ContactForm()
        return render(request, self.template_name, {'form': form, 'site_settings': SiteSettings.objects.first()})

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()

            # Send email to reservations
            subject = f"New contact message from {contact.name}"
            message = f"""
            Name: {contact.name}
            Email: {contact.email}
            Phone: {contact.phone or 'Not provided'}
            Message:
            {contact.message}
            """
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                ['reservations@villagrandemw.com'],
                fail_silently=False,
            )
            messages.success(request, 'Thank you for contacting us! We will get back to you soon.')
            return redirect('lodge:contact')
        return render(request, self.template_name, {'form': form, 'site_settings': SiteSettings.objects.first()})


class RoomListView(ListView):
    model = Room
    template_name = 'lodge/rooms.html'
    context_object_name = 'rooms'
    queryset = Room.objects.filter(is_active=True)


class RoomDetailView(DetailView):
    model = Room
    template_name = 'lodge/room_detail.html'
    context_object_name = 'room'

class AvailableRoomsView(ListView):
    model = Room
    template_name = 'lodge/available_rooms.html'
    context_object_name = 'rooms'
    paginate_by = 9

    def get_queryset(self):
        queryset = Room.objects.filter(is_active=True)

        # Get dates from GET parameters
        check_in_str = self.request.GET.get('check_in')
        check_out_str = self.request.GET.get('check_out')
        guests = self.request.GET.get('guests')

        # Store them for use in template
        self.check_in = parse_date(check_in_str) if check_in_str else None
        self.check_out = parse_date(check_out_str) if check_out_str else None
        self.guests = int(guests) if guests else 1

        # If dates are missing, redirect to home with an error message
        if not self.check_in or not self.check_out:
            messages.error(self.request, "Please select both check‑in and check‑out dates.")
            return redirect('lodge:home')

        if self.check_in >= self.check_out:
            messages.error(self.request, "Check‑out must be after check‑in.")
            return redirect('lodge:home')

        if self.check_in < timezone.now().date():
            messages.error(self.request, "Check‑in cannot be in the past.")
            return redirect('lodge:home')

        # Find all rooms that are booked during the requested period
        overlapping_bookings = Booking.objects.filter(
            status__in=['PENDING', 'CONFIRMED'],
            check_in__lt=self.check_out,
            check_out__gt=self.check_in
        ).values_list('room_id', flat=True)

        # Exclude those rooms
        queryset = queryset.exclude(id__in=overlapping_bookings)

        # Optional: filter by guest capacity if you add a `max_guests` field to Room
        # if self.guests:
        #     queryset = queryset.filter(max_guests__gte=self.guests)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['check_in'] = self.check_in
        context['check_out'] = self.check_out
        context['guests'] = self.guests
        context['search_params'] = {
            'check_in': self.check_in,
            'check_out': self.check_out,
            'guests': self.guests,
        }
        return context

class BookingCreateView(View):
    def get(self, request):
        # Pre‑fill from GET parameters – same as before
        form = ModernBookingForm()
        room_id = request.GET.get('room')
        check_in_str = request.GET.get('check_in')
        check_out_str = request.GET.get('check_out')
        guests_str = request.GET.get('guests')

        if room_id:
            try:
                room = Room.objects.get(pk=room_id, is_active=True)
                form.fields['room'].initial = room
            except Room.DoesNotExist:
                pass

        if check_in_str:
            check_in = parse_date(check_in_str)
            if check_in:
                form.fields['check_in'].initial = check_in

        if check_out_str:
            check_out = parse_date(check_out_str)
            if check_out:
                form.fields['check_out'].initial = check_out

        if guests_str:
            try:
                guests = int(guests_str)
                if 1 <= guests <= 10:
                    form.fields['guests'].initial = guests
            except ValueError:
                pass

        return render(request, 'lodge/booking.html', {'form': form})

    def post(self, request):
        form = ModernBookingForm(request.POST)
        if form.is_valid():
            # Extract cleaned data
            check_in = form.cleaned_data['check_in']
            check_out = form.cleaned_data['check_out']
            room = form.cleaned_data['room']
            guests = form.cleaned_data['guests']
            name = form.cleaned_data['name']
            phone = form.cleaned_data['phone']
            email = form.cleaned_data.get('email', '')

            # ========== CRITICAL: Use a transaction and lock the room ==========
            try:
                with transaction.atomic():
                    # Lock the room row until the transaction finishes
                    locked_room = Room.objects.select_for_update().get(pk=room.pk)

                    # Double‑check availability inside the transaction
                    overlapping = Booking.objects.filter(
                        room=locked_room,
                        check_in__lt=check_out,
                        check_out__gt=check_in,
                        status__in=['PENDING', 'CONFIRMED']
                    ).exists()

                    if overlapping:
                        # Room became unavailable between the initial check and now
                        form.add_error(None, "This room is no longer available for the selected dates.")
                        return render(request, 'lodge/booking.html', {'form': form})

                    # Optional: temporary hold / expiration (requires model field)
                    # expires_at = timezone.now() + timedelta(minutes=15)
                    # if you add an expires_at field to Booking, uncomment the line above

                    # Create or get customer
                    customer, created = Customer.objects.get_or_create(
                        phone=phone,
                        defaults={'name': name, 'email': email}
                    )

                    # Create booking (status PENDING)
                    booking = Booking.objects.create(
                        customer=customer,
                        room=locked_room,
                        check_in=check_in,
                        check_out=check_out,
                        guests=guests,
                        status='PENDING'
                        # expires_at=expires_at   # if using holds
                    )

                    # All good – commit transaction automatically

            except Room.DoesNotExist:
                form.add_error(None, "Selected room no longer exists.")
                return render(request, 'lodge/booking.html', {'form': form})

            # Send confirmation emails (outside the transaction to avoid delays)
            if customer.email:
                send_mail(
                    subject=f"Your booking with Villa Grande – {booking.booking_reference}",
                    message=f"…",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[customer.email],
                    fail_silently=False,
                )
            send_mail(
                subject=f"New Booking Request – {booking.booking_reference}",
                message=f"…",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['reservations@villagrandemw.com'],
                fail_silently=False,
            )

            return redirect('lodge:booking_success', pk=booking.pk)

        # Form invalid – re‑render with errors
        return render(request, 'lodge/booking.html', {'form': form})


class CheckBookingView(View):
    template_name = 'lodge/check_booking.html'

    def get(self, request):
        form = BookingStatusForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = BookingStatusForm(request.POST)
        if form.is_valid():
            ref = form.cleaned_data['booking_reference'].strip().upper()
            try:
                booking = Booking.objects.select_related('room', 'customer').get(booking_reference=ref)
                return render(request, self.template_name, {
                    'form': form,
                    'booking': booking,
                })
            except Booking.DoesNotExist:
                form.add_error('booking_reference', 'Booking not found. Please check your Booking ID.')
        return render(request, self.template_name, {'form': form})

class BookingSuccessView(TemplateView):
    template_name = 'lodge/booking_success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['booking'] = get_object_or_404(Booking, pk=self.kwargs['pk'])
        return context


class NewsletterSubscribeView(View):
    def post(self, request):
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for subscribing to our newsletter!')
        else:
            for error in form.errors.values():
                messages.error(request, error)
        return redirect(request.META.get('HTTP_REFERER', 'lodge:home'))

def custom_404(request, exception):
    return render(request, '404.html', status=404)

# ---------- Admin Views (Login Required) ----------
class AdminRoomListView(LoginRequiredMixin, ListView):
    model = Room
    template_name = 'lodge/admin/room_list.html'
    context_object_name = 'rooms'
    login_url = '/accounts/login/'


class AdminRoomCreateView(LoginRequiredMixin, CreateView):
    model = Room
    form_class = RoomForm
    template_name = 'lodge/admin/room_form.html'
    success_url = reverse_lazy('lodge:admin_room_list')
    login_url = '/accounts/login/'


class AdminRoomUpdateView(LoginRequiredMixin, UpdateView):
    model = Room
    form_class = RoomForm
    template_name = 'lodge/admin/room_form.html'
    success_url = reverse_lazy('lodge:admin_room_list')
    login_url = '/accounts/login/'


class AdminRoomDeleteView(LoginRequiredMixin, DeleteView):
    model = Room
    template_name = 'lodge/admin/room_confirm_delete.html'
    success_url = reverse_lazy('lodge:admin_room_list')
    login_url = '/accounts/login/'


class AdminBookingListView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'lodge/admin/booking_list.html'
    context_object_name = 'bookings'
    login_url = '/accounts/login/'
    ordering = ['-created_at']

    def get_queryset(self):
        return Booking.objects.select_related('customer', 'room').all()


class AdminBookingUpdateView(LoginRequiredMixin, UpdateView):
    model = Booking
    fields = ['status']
    template_name = 'lodge/admin/booking_form.html'
    success_url = reverse_lazy('lodge:admin_booking_list')
    login_url = '/accounts/login/'

    def form_valid(self, form):
        response = super().form_valid(form)
        if form.instance.status == 'CONFIRMED':
            send_whatsapp_confirmation(form.instance)
        return response


class AdminCustomerListView(LoginRequiredMixin, ListView):
    model = Customer
    template_name = 'lodge/admin/customer_list.html'
    context_object_name = 'customers'
    login_url = '/accounts/login/'
    paginate_by = 20
    

@staff_member_required
def admin_dashboard_stats(request):
    # Same logic as in your admin_stats template tag
    total_rooms = Room.objects.count()
    active_rooms = Room.objects.filter(is_active=True).count()
    total_bookings = Booking.objects.count()
    pending_bookings = Booking.objects.filter(status='PENDING').count()
    confirmed_bookings = Booking.objects.filter(status='CONFIRMED').count()
    total_customers = Customer.objects.count()
    newsletter_subscribers = NewsletterSubscriber.objects.filter(is_active=True).count()

    today = timezone.now().date()
    month_start = today.replace(day=1)
    monthly_revenue = 0
    for booking in Booking.objects.filter(created_at__date__gte=month_start, status='CONFIRMED'):
        if booking.room:
            monthly_revenue += booking.room.price_per_night * (booking.check_out - booking.check_in).days

    last_7_days = [(today - timedelta(days=i)) for i in range(6, -1, -1)]
    booking_trends = [Booking.objects.filter(created_at__date=d).count() for d in last_7_days]
    booking_trend_labels = [d.strftime('%a') for d in last_7_days]

    room_types = Room.objects.values('room_type').annotate(count=Count('id'))
    room_type_labels = [dict(Room.ROOM_TYPES).get(rt['room_type'], rt['room_type']) for rt in room_types]
    room_type_counts = [rt['count'] for rt in room_types]

    recent_bookings = Booking.objects.select_related('customer', 'room').order_by('-created_at')[:10]
    recent_bookings_data = [{
        'id': b.id,
        'customer': b.customer.name,
        'room': b.room.room_number,
        'check_in': b.check_in.isoformat(),
        'check_out': b.check_out.isoformat(),
        'status': b.status,
        'status_display': b.get_status_display(),
    } for b in recent_bookings]

    data = {
        'total_rooms': total_rooms,
        'active_rooms': active_rooms,
        'pending_bookings': pending_bookings,
        'confirmed_bookings': confirmed_bookings,
        'total_customers': total_customers,
        'monthly_revenue': monthly_revenue,
        'booking_trends': booking_trends,
        'booking_trend_labels': booking_trend_labels,
        'room_type_labels': room_type_labels,
        'room_type_counts': room_type_counts,
        'recent_bookings': recent_bookings_data,
    }
    return JsonResponse(data)