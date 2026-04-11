# from django.contrib.admin import AdminSite
# from django.contrib.auth.models import User, Group
# from django.contrib.auth.admin import UserAdmin, GroupAdmin
# from django.template.response import TemplateResponse
# from django.urls import path
# from .models import Room, Booking, Customer
# from .admin_models import RoomAdmin, BookingAdmin, CustomerAdmin
# from django.db.models import Count
# from django.utils import timezone
# from datetime import timedelta


# class VillaGrandeAdminSite(AdminSite):
#     site_header = 'Villa Grande Lodge Management'
#     site_title  = 'Villa Grande CMS'
#     index_title = 'Dashboard'
#     site_url    = '/'

#     # ── Point every built-in admin view at our themed templates ─────────────
#     index_template            = 'admin/villagrande/dashboard.html'
#     login_template            = 'admin/villagrande/login.html'
#     logout_template           = 'admin/villagrande/logout.html'
#     change_list_template      = 'admin/villagrande/change_list.html'
#     change_form_template      = 'admin/villagrande/change_form.html'
#     delete_confirmation_template          = 'admin/villagrande/delete_confirmation.html'
#     delete_selected_confirmation_template = 'admin/villagrande/delete_confirmation.html'
#     object_history_template   = 'admin/villagrande/object_history.html'

#     def get_urls(self):
#         urls = super().get_urls()
#         custom_urls = [
#             path('analytics/',     self.admin_view(self.analytics_view),     name='analytics'),
#             path('notifications/', self.admin_view(self.notifications_view), name='notifications'),
#         ]
#         return custom_urls + urls

#     # ── Shared stats ─────────────────────────────────────────────────────────
#     def _base_context(self):
#         from .models import NewsletterSubscriber

#         total_rooms        = Room.objects.count()
#         active_rooms       = Room.objects.filter(is_active=True).count()
#         total_bookings     = Booking.objects.count()
#         pending_bookings   = Booking.objects.filter(status='PENDING').count()
#         confirmed_bookings = Booking.objects.filter(status='CONFIRMED').count()
#         cancelled_bookings = Booking.objects.filter(status='CANCELLED').count()
#         total_customers    = Customer.objects.count()
#         newsletter_subscribers = NewsletterSubscriber.objects.filter(is_active=True).count()

#         today       = timezone.now().date()
#         month_start = today.replace(day=1)
#         monthly_revenue = 0
#         for booking in Booking.objects.filter(created_at__date__gte=month_start, status='CONFIRMED'):
#             if booking.room:
#                 monthly_revenue += booking.room.price_per_night * (booking.check_out - booking.check_in).days

#         last_7_days    = [(today - timedelta(days=i)) for i in range(6, -1, -1)]
#         booking_trends = [Booking.objects.filter(created_at__date=d).count() for d in last_7_days]

#         room_types       = Room.objects.values('room_type').annotate(count=Count('id'))
#         room_type_labels = [dict(Room.ROOM_TYPES).get(rt['room_type'], rt['room_type']) for rt in room_types]
#         room_type_counts = [rt['count'] for rt in room_types]

#         return {
#             'total_rooms':            total_rooms,
#             'active_rooms':           active_rooms,
#             'total_bookings':         total_bookings,
#             'pending_bookings':       pending_bookings,
#             'confirmed_bookings':     confirmed_bookings,
#             'cancelled_bookings':     cancelled_bookings,
#             'total_customers':        total_customers,
#             'newsletter_subscribers': newsletter_subscribers,
#             'monthly_revenue':        monthly_revenue,
#             'booking_trends':         booking_trends,
#             'booking_trend_labels':   [d.strftime('%a') for d in last_7_days],
#             'room_type_labels':       room_type_labels,
#             'room_type_counts':       room_type_counts,
#         }

#     # ── Views ────────────────────────────────────────────────────────────────
#     def index(self, request, extra_context=None):
#         context = self._base_context()
#         context['recent_bookings'] = (
#             Booking.objects.select_related('customer', 'room').order_by('-created_at')[:10]
#         )
#         if extra_context:
#             context.update(extra_context)
#         return TemplateResponse(request, self.index_template, context)

#     def analytics_view(self, request):
#         context = self._base_context()
#         context['title'] = 'Analytics'
#         return TemplateResponse(request, 'admin/villagrande/analytics.html', context)

#     def notifications_view(self, request):
#         return TemplateResponse(request, 'admin/villagrande/notifications.html', {'title': 'Notifications'})


# # ── Create instance & register models ───────────────────────────────────────
# admin_site = VillaGrandeAdminSite(name='villagrande_admin')

# admin_site.register(User,     UserAdmin)
# admin_site.register(Group,    GroupAdmin)
# admin_site.register(Room,     RoomAdmin)
# admin_site.register(Booking,  BookingAdmin)
# admin_site.register(Customer, CustomerAdmin)

# # Dynamic content models — must come AFTER admin_site is created
# from . import admin_dynamic  # noqa: E402, F401

from django.contrib.admin import AdminSite
from django.template.response import TemplateResponse
from django.urls import path
from .models import Room, Booking, Customer
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta

class VillaGrandeAdminSite(AdminSite):
    site_header = 'Villa Grande Lodge Management'
    site_title = 'Villa Grande CMS'
    index_title = 'Dashboard'

    def index(self, request, extra_context=None):
        # Compute stats (same as before)
        total_rooms = Room.objects.count()
        active_rooms = Room.objects.filter(is_active=True).count()
        total_bookings = Booking.objects.count()
        pending_bookings = Booking.objects.filter(status='PENDING').count()
        confirmed_bookings = Booking.objects.filter(status='CONFIRMED').count()
        cancelled_bookings = Booking.objects.filter(status='CANCELLED').count()
        total_customers = Customer.objects.count()

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

        context = {
            **self.each_context(request),
            'total_rooms': total_rooms,
            'active_rooms': active_rooms,
            'total_bookings': total_bookings,
            'pending_bookings': pending_bookings,
            'confirmed_bookings': confirmed_bookings,
            'cancelled_bookings': cancelled_bookings,
            'total_customers': total_customers,
            'monthly_revenue': monthly_revenue,
            'booking_trends': booking_trends,
            'booking_trend_labels': booking_trend_labels,
            'room_type_labels': room_type_labels,
            'room_type_counts': room_type_counts,
            'recent_bookings': recent_bookings,
        }
        if extra_context:
            context.update(extra_context)
        return TemplateResponse(request, self.index_template or 'admin/index.html', context)

admin_site = VillaGrandeAdminSite(name='myadmin')