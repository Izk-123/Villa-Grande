from django.contrib.admin import AdminSite
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.template.response import TemplateResponse
from django.urls import path
from .models import Room, Booking, Customer
from .admin_models import RoomAdmin, BookingAdmin, CustomerAdmin
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta

class VillaGrandeAdminSite(AdminSite):
    site_header = 'Villa Grande Lodge Management'
    site_title = 'Villa Grande CMS'
    index_title = 'Dashboard'
    site_url = '/'
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('analytics/', self.admin_view(self.analytics_view), name='analytics'),
            path('notifications/', self.admin_view(self.notifications_view), name='notifications'),
        ]
        return custom_urls + urls
    
    def index(self, request, extra_context=None):
        # Get statistics
        total_rooms = Room.objects.count()
        active_rooms = Room.objects.filter(is_active=True).count()
        total_bookings = Booking.objects.count()
        pending_bookings = Booking.objects.filter(status='PENDING').count()
        confirmed_bookings = Booking.objects.filter(status='CONFIRMED').count()
        total_customers = Customer.objects.count()
        
        # Recent bookings
        recent_bookings = Booking.objects.select_related('customer', 'room').order_by('-created_at')[:10]
        
        # Monthly revenue
        today = timezone.now().date()
        month_start = today.replace(day=1)
        monthly_bookings = Booking.objects.filter(
            created_at__date__gte=month_start,
            status='CONFIRMED'
        )
        monthly_revenue = 0
        for booking in monthly_bookings:
            if booking.room:
                nights = (booking.check_out - booking.check_in).days
                monthly_revenue += booking.room.price_per_night * nights
        
        # Booking trends (last 7 days)
        last_7_days = [(today - timedelta(days=i)) for i in range(6, -1, -1)]
        booking_trends = []
        for day in last_7_days:
            count = Booking.objects.filter(created_at__date=day).count()
            booking_trends.append(count)
        
        # Room occupancy by type
        room_types = Room.objects.values('room_type').annotate(count=Count('id'))
        room_type_labels = []
        room_type_counts = []
        for rt in room_types:
            room_type_labels.append(dict(Room.ROOM_TYPES).get(rt['room_type'], rt['room_type']))
            room_type_counts.append(rt['count'])
        
        context = {
            'total_rooms': total_rooms,
            'active_rooms': active_rooms,
            'total_bookings': total_bookings,
            'pending_bookings': pending_bookings,
            'confirmed_bookings': confirmed_bookings,
            'total_customers': total_customers,
            'monthly_revenue': monthly_revenue,
            'recent_bookings': recent_bookings,
            'booking_trends': booking_trends,
            'booking_trend_labels': [day.strftime('%a') for day in last_7_days],
            'room_type_labels': room_type_labels,
            'room_type_counts': room_type_counts,
        }
        
        if extra_context:
            context.update(extra_context)
        
        return TemplateResponse(request, 'admin/villagrande/dashboard.html', context)
    
    def analytics_view(self, request):
        context = {
            'title': 'Analytics',
        }
        return TemplateResponse(request, 'admin/villagrande/analytics.html', context)
    
    def notifications_view(self, request):
        context = {
            'title': 'Notifications',
        }
        return TemplateResponse(request, 'admin/villagrande/notifications.html', context)

# Create the admin site instance
admin_site = VillaGrandeAdminSite(name='villagrande_admin')

# Register your models
admin_site.register(User, UserAdmin)
admin_site.register(Group, GroupAdmin)
admin_site.register(Room, RoomAdmin)
admin_site.register(Booking, BookingAdmin)
admin_site.register(Customer, CustomerAdmin)