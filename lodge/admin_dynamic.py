from django.contrib import admin
from .admin_site import admin_site
from .models import (
    ContactMessage, HeroSlide, AboutSection, Statistic,
    Service, ExperienceSection, Testimonial,
    NewsletterSection, NewsletterSubscriber, SiteSettings
)


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
        (None, {
            'fields': ('title', 'subtitle', 'description', 'is_active')
        }),
        ('Images', {
            'fields': ('image_main', 'image_accent'),
        }),
        ('Settings', {
            'fields': ('years_of_excellence', 'button_text', 'button_link'),
        }),
    )


class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'icon', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title', 'description']


class ExperienceSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active']
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'background_image', 'video_url', 'is_active')
        }),
        ('Buttons', {
            'fields': ('button_one_text', 'button_one_link', 'button_two_text', 'button_two_link'),
        }),
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
    # Use fieldsets to organise the form
    fieldsets = (
        ('Branding', {
            'fields': ('site_name', 'tagline', 'logo')
        }),
        ('Contact Information', {
            'fields': ('address', 'phone', 'email', 'whatsapp')
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'instagram_url', 'twitter_url', 'youtube_url')
        }),
        ('Footer', {
            'fields': ('copyright_text',)
        }),
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

# Register all dynamic content models with the custom Villa Grande admin site


admin.site.register(HeroSlide, HeroSlideAdmin)
admin.site.register(AboutSection, AboutSectionAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(ExperienceSection, ExperienceSectionAdmin)
admin.site.register(Testimonial, TestimonialAdmin)
admin.site.register(NewsletterSection, NewsletterSectionAdmin)
admin.site.register(NewsletterSubscriber, NewsletterSubscriberAdmin)
admin.site.register(SiteSettings, SiteSettingsAdmin)
admin.site.register(ContactMessage, ContactMessageAdmin)