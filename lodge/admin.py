# lodge/admin.py
from django.contrib import admin
from .models import (
    Room, Customer, Booking,
    ContactMessage, HeroSlide, AboutSection, Statistic,
    Service, ExperienceSection, Testimonial,
    NewsletterSection, NewsletterSubscriber, SiteSettings, Amenity
)

from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

User = get_user_model()

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # You can customize the fields shown in the change form
    fieldsets = UserAdmin.fieldsets  # keep the default fieldsets
    # Or limit to only the fields you want:
    # fieldsets = (
    #     (None, {'fields': ('username', 'password')}),
    #     ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
    #     ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    #     ('Important dates', {'fields': ('last_login', 'date_joined')}),
    # )

# ---------- Room, Customer, Booking ----------
class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_number', 'room_type', 'price_per_night', 'is_active']
    list_filter = ['room_type', 'is_active']
    search_fields = ['room_number', 'description']
    list_editable = ['price_per_night', 'is_active']
    filter_horizontal = ['amenities']
    fieldsets = (
        (None, {'fields': ('room_number', 'room_type', 'price_per_night', 'is_active')}),
        ('Details', {'fields': ('description', 'image'), 'classes': ('wide',)}),
    )

class AmenityAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon_class', 'is_active']
    list_editable = ['is_active']

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'created_at']
    search_fields = ['name', 'phone', 'email']
    list_filter = ['created_at']
    date_hierarchy = 'created_at'

class BookingAdmin(admin.ModelAdmin):
    list_display = [
        'booking_reference',   # <-- added
        'id',                  # keep if you want both; you can remove 'id' if preferred
        'customer',
        'room',
        'check_in',
        'check_out',
        'status',
        'created_at'
    ]
    list_filter = ['status', 'check_in', 'check_out']
    search_fields = [
        'booking_reference',   # <-- added
        'customer__name',
        'customer__phone',
        'room__room_number'
    ]
    date_hierarchy = 'check_in'
    list_editable = ['status']
    raw_id_fields = ['customer', 'room']
    readonly_fields = ['booking_reference']   # <-- added (prevents editing)

    fieldsets = (
        (None, {'fields': ('booking_reference', 'customer', 'room', 'status')}),  # <-- added reference
        ('Dates', {'fields': ('check_in', 'check_out', 'guests'), 'classes': ('wide',)}),
    )

    actions = ['confirm_bookings', 'cancel_bookings']

    def confirm_bookings(self, request, queryset):
        queryset.update(status='CONFIRMED')
    confirm_bookings.short_description = "Confirm selected bookings"

    def cancel_bookings(self, request, queryset):
        queryset.update(status='CANCELLED')
    cancel_bookings.short_description = "Cancel selected bookings"

# ---------- Dynamic content models ----------
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title', 'subtitle']

class StatisticInline(admin.TabularInline):
    model = Statistic
    extra = 1

class AboutSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active']
    inlines = [StatisticInline]
    fieldsets = (
        (None, {'fields': ('title', 'subtitle', 'description', 'is_active')}),
        ('Images', {'fields': ('image_main', 'image_accent')}),
        ('Settings', {'fields': ('years_of_excellence', 'button_text', 'button_link')}),
    )

class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'icon', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title', 'description']

class ExperienceSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active']
    fieldsets = (
        (None, {'fields': ('title', 'description', 'background_image', 'video_url', 'is_active')}),
        ('Buttons', {'fields': ('button_one_text', 'button_one_link', 'button_two_text', 'button_two_link')}),
    )

class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'rating', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['rating', 'is_active']
    search_fields = ['name', 'text']

class NewsletterSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active']

class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'subscribed_at', 'is_active']
    list_filter = ['is_active']
    search_fields = ['email']
    readonly_fields = ['subscribed_at']

class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Branding', {'fields': ('site_name', 'tagline', 'logo')}),
        ('Contact Information', {'fields': ('address', 'phone', 'email', 'whatsapp')}),
        ('Social Media', {'fields': ('facebook_url', 'instagram_url', 'twitter_url', 'youtube_url')}),
        ('Footer', {'fields': ('copyright_text',)}),
    )

class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'created_at', 'is_read']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'message']
    readonly_fields = ['created_at']
    actions = ['mark_as_read']

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected messages as read"

# Register everything with the default admin site
admin.site.register(Room, RoomAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(HeroSlide, HeroSlideAdmin)
admin.site.register(AboutSection, AboutSectionAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(ExperienceSection, ExperienceSectionAdmin)
admin.site.register(Testimonial, TestimonialAdmin)
admin.site.register(NewsletterSection, NewsletterSectionAdmin)
admin.site.register(NewsletterSubscriber, NewsletterSubscriberAdmin)
admin.site.register(SiteSettings, SiteSettingsAdmin)
admin.site.register(ContactMessage, ContactMessageAdmin)
admin.site.register(Amenity, AmenityAdmin)