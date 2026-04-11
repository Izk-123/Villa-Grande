# accounts/views.py (relevant parts)

from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView, ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.decorators import login_required
from .models import User, Role, Permission
from .mixins import PermissionRequiredMixin
from .forms import CustomUserCreationForm, UserUpdateForm
from lodge.models import Room, Booking, Customer
from datetime import timedelta
from django.utils import timezone
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import logout

# ---------- Auth ----------
class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('accounts:dashboard')


class UserLogoutView(LogoutView):
    http_method_names = ['get', 'post', 'options']
    next_page = 'accounts:login'

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(self.next_page)


# ---------- Dashboard ----------
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        now = timezone.now()
        today = now.date()
        start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        # Calculate monthly revenue manually
        monthly_revenue = 0
        confirmed_bookings = Booking.objects.filter(
            status='CONFIRMED',
            created_at__gte=start_of_month,
            created_at__lte=now
        ).select_related('room')

        for booking in confirmed_bookings:
            nights = (booking.check_out - booking.check_in).days
            monthly_revenue += booking.room.price_per_night * nights

        stats = {
            'total_rooms': Room.objects.count(),
            'active_rooms': Room.objects.filter(is_active=True).count(),
            'pending_bookings': Booking.objects.filter(status='PENDING').count(),
            'confirmed_bookings': Booking.objects.filter(status='CONFIRMED').count(),
            'total_customers': Customer.objects.count(),
            'monthly_revenue': monthly_revenue,
        }

        # Booking trends (last 7 days)
        last_7_days = [(today - timedelta(days=i)) for i in range(6, -1, -1)]
        booking_trends = []
        for d in last_7_days:
            count = Booking.objects.filter(created_at__date=d).count()
            booking_trends.append(count)
        stats['booking_trends'] = booking_trends
        stats['booking_trend_labels'] = [d.strftime('%a') for d in last_7_days]

        # Room type distribution (using the ROOM_TYPES choices)
        type_counts = Room.objects.values('room_type').annotate(count=Count('id'))
        type_dict = dict(Room.ROOM_TYPES)
        stats['room_type_labels'] = [type_dict.get(rt['room_type'], rt['room_type']) for rt in type_counts]
        stats['room_type_counts'] = [rt['count'] for rt in type_counts]

        # Recent bookings
        stats['recent_bookings'] = Booking.objects.select_related('customer', 'room').order_by('-created_at')[:10]

        context['stats'] = stats
        return context


# ---------- User Management (Admin only) ----------
class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = User
    template_name = 'accounts/user_list.html'
    context_object_name = 'users'
    permission_required = 'manage_users'


class UserCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('accounts:user_list')
    permission_required = 'manage_users'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'User {form.instance.username} created successfully.')
        return response


class UserUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('accounts:user_list')
    permission_required = 'manage_users'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'User {form.instance.username} updated successfully.')
        return response


@login_required
def live_stats(request):
    now = timezone.now()
    today = now.date()
    start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    # Calculate monthly revenue manually
    monthly_revenue = 0
    confirmed_bookings = Booking.objects.filter(
        status='CONFIRMED',
        created_at__gte=start_of_month,
        created_at__lte=now
    ).select_related('room')

    for booking in confirmed_bookings:
        nights = (booking.check_out - booking.check_in).days
        monthly_revenue += booking.room.price_per_night * nights

    data = {
        'total_rooms': Room.objects.count(),
        'active_rooms': Room.objects.filter(is_active=True).count(),
        'pending_bookings': Booking.objects.filter(status='PENDING').count(),
        'confirmed_bookings': Booking.objects.filter(status='CONFIRMED').count(),
        'total_customers': Customer.objects.count(),
        'monthly_revenue': monthly_revenue,
    }

    # Booking trends (last 7 days)
    last_7_days = [(today - timedelta(days=i)) for i in range(6, -1, -1)]
    booking_trends = []
    for d in last_7_days:
        count = Booking.objects.filter(created_at__date=d).count()
        booking_trends.append(count)
    data['booking_trends'] = booking_trends
    data['booking_trend_labels'] = [d.strftime('%a') for d in last_7_days]

    # Room type distribution (using the ROOM_TYPES choices)
    type_counts = Room.objects.values('room_type').annotate(count=Count('id'))
    type_dict = dict(Room.ROOM_TYPES)
    data['room_type_labels'] = [type_dict.get(rt['room_type'], rt['room_type']) for rt in type_counts]
    data['room_type_counts'] = [rt['count'] for rt in type_counts]

    # Recent bookings (as list of dicts)
    recent_bookings = Booking.objects.select_related('customer', 'room').order_by('-created_at')[:10]
    data['recent_bookings'] = [{
        'id': b.id,
        'customer': b.customer.name,
        'room': b.room.room_number,
        'check_in': b.check_in.isoformat(),
        'check_out': b.check_out.isoformat(),
        'status': b.status,
        'status_display': b.get_status_display(),
    } for b in recent_bookings]

    return JsonResponse(data)


@login_required
@csrf_exempt
def user_update_role(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = data.get('user_id')
        role_id = data.get('role_id')
        try:
            user = User.objects.get(id=user_id)
            from .models import Role
            role = Role.objects.get(id=role_id) if role_id else None
            user.profile.role = role
            user.profile.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid method'})