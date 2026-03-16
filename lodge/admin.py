# from django.contrib import admin
# from .models import Room, Customer, Booking

# @admin.register(Room)
# class RoomAdmin(admin.ModelAdmin):
#     list_display = ['room_number', 'room_type', 'price_per_night', 'is_active']
#     list_filter = ['room_type', 'is_active']

# @admin.register(Customer)
# class CustomerAdmin(admin.ModelAdmin):
#     list_display = ['name', 'phone', 'email', 'created_at']
#     search_fields = ['name', 'phone', 'email']

# @admin.register(Booking)
# class BookingAdmin(admin.ModelAdmin):
#     list_display = ['id', 'customer', 'room', 'check_in', 'check_out', 'status']
#     list_filter = ['status', 'check_in', 'check_out']
#     date_hierarchy = 'check_in'