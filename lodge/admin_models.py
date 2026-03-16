from django.contrib import admin
from .models import Room, Customer, Booking

class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_number', 'room_type', 'price_per_night', 'is_active']
    list_filter = ['room_type', 'is_active']
    search_fields = ['room_number', 'description']
    list_editable = ['price_per_night', 'is_active']
    
    fieldsets = (
        (None, {
            'fields': ('room_number', 'room_type', 'price_per_night', 'is_active')
        }),
        ('Details', {
            'fields': ('description', 'image'),
            'classes': ('wide',)
        }),
    )

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'created_at']
    search_fields = ['name', 'phone', 'email']
    list_filter = ['created_at']
    date_hierarchy = 'created_at'

class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'room', 'check_in', 'check_out', 'status', 'created_at']
    list_filter = ['status', 'check_in', 'check_out']
    search_fields = ['customer__name', 'customer__phone', 'room__room_number']
    date_hierarchy = 'check_in'
    list_editable = ['status']
    raw_id_fields = ['customer', 'room']
    
    fieldsets = (
        (None, {
            'fields': ('customer', 'room', 'status')
        }),
        ('Dates', {
            'fields': ('check_in', 'check_out', 'guests'),
            'classes': ('wide',)
        }),
    )
    
    actions = ['confirm_bookings', 'cancel_bookings']
    
    def confirm_bookings(self, request, queryset):
        queryset.update(status='CONFIRMED')
    confirm_bookings.short_description = "Confirm selected bookings"
    
    def cancel_bookings(self, request, queryset):
        queryset.update(status='CANCELLED')
    cancel_bookings.short_description = "Cancel selected bookings"