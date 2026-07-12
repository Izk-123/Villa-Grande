# lodge/admin.py - Django Admin Configuration for Villa Grande Lodge
# ------------------------------------------------------------------------------
# This file customizes the Django admin interface to provide a polished,
# user-friendly experience for the lodge staff. It includes custom widgets,
# refined layouts, curated selections, and now supports multiple room images
# via an inline formset and a custom IconPickerWidget for amenities.
# ------------------------------------------------------------------------------

from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html, escape
from django.utils.safestring import mark_safe

from .models import (
    Room, Customer, Booking, ContactMessage,
    HeroSlide, AboutSection, Statistic, Service,
    ExperienceSection, Testimonial, NewsletterSection,
    NewsletterSubscriber, SiteSettings, Amenity,
    RoomImage  # <-- Import the new RoomImage model for gallery
)

# ------------------------------------------------------------------------------
# 1. Custom User Admin
# ------------------------------------------------------------------------------

User = get_user_model()

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Extends the default Django User Admin.
    Keeps default fieldsets for full flexibility; can be overridden if needed.
    """
    pass


# ------------------------------------------------------------------------------
# 2. Room, Customer, and Booking Admins
# ------------------------------------------------------------------------------

class RoomImageInline(admin.TabularInline):
    """
    Inline admin for RoomImage. Allows staff to upload, reorder, and delete
    multiple gallery images directly inside the Room add/change page.
    """
    model = RoomImage
    extra = 1                     # Show one empty row by default
    fields = ['image', 'order']   # Order field controls the sort order for the carousel
    show_change_link = True       # Optional: link to the individual image admin if needed
    verbose_name = "Gallery Image"
    verbose_name_plural = "Gallery Images"


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    """
    Admin configuration for Rooms.
    Uses a dual-list selector (filter_horizontal) for ManyToMany amenities
    and now includes an inline tabular formset for multiple gallery images.
    """
    inlines = [RoomImageInline]   # <-- Add the inline for gallery images

    list_display = ['room_number', 'room_type', 'price_per_night', 'is_active']
    list_filter = ['room_type', 'is_active']
    search_fields = ['room_number', 'description']
    list_editable = ['price_per_night', 'is_active']

    # Renders a user-friendly horizontal two-pane selector for amenities
    filter_horizontal = ['amenities']

    fieldsets = (
        (None, {
            'fields': ('room_number', 'room_type', 'price_per_night', 'is_active')
        }),
        ('Details', {
            'fields': ('description', 'image', 'amenities'),
            'classes': ('wide',)
        }),
    )


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """Admin configuration for Customers."""
    list_display = ['name', 'phone', 'email', 'created_at']
    search_fields = ['name', 'phone', 'email']
    list_filter = ['created_at']
    date_hierarchy = 'created_at'


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """
    Admin configuration for Bookings.
    Includes the unique booking_reference field (readonly) and bulk actions.
    """
    list_display = [
        'booking_reference', 'id', 'customer', 'room',
        'check_in', 'check_out', 'status', 'created_at'
    ]
    list_filter = ['status', 'check_in', 'check_out']
    search_fields = [
        'booking_reference', 'customer__name',
        'customer__phone', 'room__room_number'
    ]
    date_hierarchy = 'check_in'
    list_editable = ['status']
    raw_id_fields = ['customer', 'room']
    readonly_fields = ['booking_reference']  # Prevent manual editing

    fieldsets = (
        (None, {
            'fields': ('booking_reference', 'customer', 'room', 'status')
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


# ------------------------------------------------------------------------------
# 3. Amenity Admin with Custom Icon Picker Widget
# ------------------------------------------------------------------------------

# Curated list of Font Awesome icons relevant for a lodge.
# Staff can click a visual chip rather than memorizing CSS class names.
AMENITY_ICON_SUGGESTIONS = [
    ('fas fa-wifi', 'Free WiFi'),
    ('fas fa-swimming-pool', 'Swimming Pool'),
    ('fas fa-parking', 'Free Parking'),
    ('fas fa-snowflake', 'Air Conditioning'),
    ('fas fa-tv', 'Flat-screen TV'),
    ('fas fa-mug-hot', 'Coffee / Tea Maker'),
    ('fas fa-utensils', 'Breakfast Included'),
    ('fas fa-dumbbell', 'Gym Access'),
    ('fas fa-spa', 'Spa Access'),
    ('fas fa-glass-martini-alt', 'Mini Bar'),
    ('fas fa-concierge-bell', '24/7 Room Service'),
    ('fas fa-shower', 'Rain Shower'),
    ('fas fa-bath', 'Bathtub'),
    ('fas fa-bed', 'King-size Bed'),
    ('fas fa-fan', 'Ceiling Fan'),
    ('fas fa-fire', 'Fireplace'),
    ('fas fa-tshirt', 'Laundry Service'),
    ('fas fa-wheelchair', 'Wheelchair Accessible'),
    ('fas fa-paw', 'Pet Friendly'),
    ('fas fa-smoking-ban', 'Non-Smoking'),
    ('fas fa-shuttle-van', 'Airport Shuttle'),
    ('fas fa-umbrella-beach', 'Beach Access'),
    ('fas fa-mountain', 'Mountain View'),
    ('fas fa-water', 'Lake / Ocean View'),
    ('fas fa-baby', 'Baby Crib Available'),
    ('fas fa-lock', 'In-room Safe'),
    ('fas fa-phone', 'Telephone'),
    ('fas fa-door-open', 'Private Balcony'),
    ('fas fa-soap', 'Toiletries Provided'),
    ('fas fa-car', 'Car Rental / Valet'),
]


class IconPickerWidget(forms.TextInput):
    """
    A custom widget that renders a live icon preview and a clickable grid
    of curated icons. Staff click the chip -> the input field auto-fills
    with the correct Font Awesome class name.
    It also includes a fallback text input with datalist for custom icons.
    """
    def render(self, name, value, attrs=None, renderer=None):
        input_html = super().render(name, value, attrs, renderer)
        widget_id = (attrs or {}).get('id') or f'id_{name}'
        safe_value = escape(value or 'fas fa-question-circle')

        # Generate datalist options
        options_html = ''.join(
            f'<option value="{escape(cls)}">{escape(label)}</option>'
            for cls, label in AMENITY_ICON_SUGGESTIONS
        )
        # Generate clickable chips
        chips_html = ''.join(
            f'<button type="button" class="icon-picker-chip" data-icon="{escape(cls)}" title="{escape(label)}">'
            f'<i class="{escape(cls)}"></i><span>{escape(label)}</span>'
            f'</button>'
            for cls, label in AMENITY_ICON_SUGGESTIONS
        )

        return mark_safe(f'''
            <div class="icon-picker">
                <div class="icon-picker-row">
                    <span class="icon-picker-preview" id="{widget_id}_preview">
                        <i class="{safe_value}"></i>
                    </span>
                    <div class="icon-picker-input-wrap">
                        {input_html}
                        <datalist id="{widget_id}_list">{options_html}</datalist>
                        <small class="icon-picker-hint">
                            Click an icon below, or type your own if you don't see what you need.
                        </small>
                    </div>
                </div>
                <div class="icon-picker-grid">{chips_html}</div>
            </div>
            <style>
                .icon-picker-row {{ display: flex; align-items: flex-start; gap: 14px; margin-bottom: 10px; }}
                .icon-picker-preview {{
                    flex-shrink: 0; width: 46px; height: 46px; display: flex; align-items: center; justify-content: center;
                    border: 1px solid #ddd; border-radius: 10px; font-size: 1.3rem; color: #C9A84C; background: #fafafa;
                }}
                .icon-picker-input-wrap {{ flex: 1; min-width: 200px; }}
                .icon-picker-hint {{ display: block; color: #888; margin-top: 4px; }}
                .icon-picker-grid {{
                    display: grid; grid-template-columns: repeat(auto-fill, minmax(120px, 1fr)); gap: 6px;
                    max-height: 220px; overflow-y: auto; padding: 10px; border: 1px solid #eee; border-radius: 10px; background: #fcfcfc;
                }}
                .icon-picker-chip {{
                    display: flex; align-items: center; gap: 8px; padding: 7px 9px; font-size: 0.78rem;
                    border: 1px solid #e2e2e2; border-radius: 8px; background: #fff; cursor: pointer; text-align: left;
                    transition: all 0.15s ease;
                }}
                .icon-picker-chip i {{ color: #C9A84C; width: 16px; text-align: center; }}
                .icon-picker-chip:hover {{ border-color: #C9A84C; background: #fff9ec; transform: translateY(-1px); }}
                .icon-picker-chip.is-selected {{ border-color: #C9A84C; background: #C9A84C; color: #0A2342; }}
                .icon-picker-chip.is-selected i {{ color: #0A2342; }}
            </style>
            <script>
            (function() {{
                var input = document.getElementById("{widget_id}");
                var preview = document.getElementById("{widget_id}_preview");
                if (!input) return;
                input.setAttribute("list", "{widget_id}_list");
                input.setAttribute("placeholder", "e.g. fas fa-wifi");

                function refreshPreview() {{
                    if (preview) preview.innerHTML = '<i class="' + (input.value || "fas fa-question-circle") + '"></i>';
                    document.querySelectorAll('#{widget_id}_wrap .icon-picker-chip, .icon-picker-chip').forEach(function(chip) {{
                        chip.classList.toggle('is-selected', chip.getAttribute('data-icon') === input.value);
                    }});
                }}
                input.addEventListener('input', refreshPreview);

                document.querySelectorAll('.icon-picker-chip').forEach(function(chip) {{
                    chip.addEventListener('click', function() {{
                        input.value = chip.getAttribute('data-icon');
                        refreshPreview();
                    }});
                }});
                refreshPreview();
            }})();
            </script>
        ''')


class AmenityAdminForm(forms.ModelForm):
    """ModelForm that applies the IconPickerWidget to the icon_class field."""
    class Meta:
        model = Amenity
        fields = '__all__'
        widgets = {
            'icon_class': IconPickerWidget(attrs={'class': 'form-control'}),
        }


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    """
    Admin configuration for Amenities.
    Uses the custom AmenityAdminForm with the IconPickerWidget.
    Loads Font Awesome for the changelist preview.
    """
    form = AmenityAdminForm
    list_display = ['icon_preview', 'name', 'is_active']
    list_editable = ['is_active']
    search_fields = ['name']
    ordering = ['name']
    list_per_page = 50

    class Media:
        css = {
            'all': ('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css',)
        }

    def icon_preview(self, obj):
        """Displays the actual Font Awesome icon in the changelist."""
        return format_html(
            '<i class="{}" style="font-size:1.3rem; color:#C9A84C;" title="{}"></i>',
            obj.icon_class or 'fas fa-question-circle', obj.icon_class
        )
    icon_preview.short_description = 'Icon'


# ------------------------------------------------------------------------------
# 4. Dynamic Content Admins (Homepage Sections)
# ------------------------------------------------------------------------------

@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    """Admin for hero carousel slides on the homepage."""
    list_display = ['title', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title', 'subtitle']


class StatisticInline(admin.TabularInline):
    """Inline for Statistics inside the About section."""
    model = Statistic
    extra = 1


@admin.register(AboutSection)
class AboutSectionAdmin(admin.ModelAdmin):
    """Admin for the 'About Us' section content, with inline statistics."""
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


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """Admin for Services displayed on the homepage."""
    list_display = ['title', 'icon', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title', 'description']


@admin.register(ExperienceSection)
class ExperienceSectionAdmin(admin.ModelAdmin):
    """Admin for the 'Experience' section (video/background image)."""
    list_display = ['title', 'is_active']
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'background_image', 'video_url', 'is_active')
        }),
        ('Buttons', {
            'fields': ('button_one_text', 'button_one_link', 'button_two_text', 'button_two_link'),
        }),
    )


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    """Admin for guest testimonials."""
    list_display = ['name', 'location', 'rating', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['rating', 'is_active']
    search_fields = ['name', 'text']


@admin.register(NewsletterSection)
class NewsletterSectionAdmin(admin.ModelAdmin):
    """Admin for the Newsletter signup section copy."""
    list_display = ['title', 'is_active']


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    """Admin for managing newsletter subscribers."""
    list_display = ['email', 'subscribed_at', 'is_active']
    list_filter = ['is_active']
    search_fields = ['email']
    readonly_fields = ['subscribed_at']


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    """
    Admin for global site settings (contact info, branding, social links).
    Since there should only be one instance, the model's save() method
    handles enforcing that logic.
    """
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


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """Admin for incoming contact form messages."""
    list_display = ['name', 'email', 'created_at', 'is_read']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'message']
    readonly_fields = ['created_at']
    actions = ['mark_as_read']

    def mark_as_read(self, request, queryset):
        """Bulk action to mark selected messages as read."""
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected messages as read"