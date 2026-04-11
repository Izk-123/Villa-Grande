from django import template
from django.utils import timezone
from datetime import timedelta
from lodge.models import Room, Booking, Customer, NewsletterSubscriber
from django.db.models import Count

register = template.Library()

@register.simple_tag
def get_admin_stats():
    total_rooms = Room.objects.count()
    active_rooms = Room.objects.filter(is_active=True).count()
    total_bookings = Booking.objects.count()
    pending_bookings = Booking.objects.filter(status='PENDING').count()
    confirmed_bookings = Booking.objects.filter(status='CONFIRMED').count()
    cancelled_bookings = Booking.objects.filter(status='CANCELLED').count()
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

    return {
        'total_rooms': total_rooms,
        'active_rooms': active_rooms,
        'total_bookings': total_bookings,
        'pending_bookings': pending_bookings,
        'confirmed_bookings': confirmed_bookings,
        'cancelled_bookings': cancelled_bookings,
        'total_customers': total_customers,
        'newsletter_subscribers': newsletter_subscribers,
        'monthly_revenue': monthly_revenue,
        'booking_trends': booking_trends,
        'booking_trend_labels': booking_trend_labels,
        'room_type_labels': room_type_labels,
        'room_type_counts': room_type_counts,
        'recent_bookings': recent_bookings,
    }