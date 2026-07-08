from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import random
import string

class Amenity(models.Model):
    name = models.CharField(max_length=100)
    icon_class = models.CharField(max_length=50, help_text='Font Awesome class, e.g., fas fa-wifi')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Room(models.Model):
    ROOM_TYPES = [
        ('STD', 'Standard'),
        ('DLX', 'Deluxe'),
        ('EXE', 'Executive'),
        ('PRE', 'Presidential'),
    ]
    room_number = models.CharField(max_length=10, unique=True)
    room_type = models.CharField(max_length=3, choices=ROOM_TYPES)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='rooms/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    amenities = models.ManyToManyField(Amenity, blank=True)

    def __str__(self):
        return f"{self.room_number} - {self.get_room_type_display()}"


class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Booking(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='bookings')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    check_in = models.DateField()
    check_out = models.DateField()
    guests = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(10)])
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    booking_reference = models.CharField(max_length=20, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.booking_reference:
            self.booking_reference = self.generate_booking_reference()
        super().save(*args, **kwargs)

    def generate_booking_reference(self):
        """Generate a unique booking reference like VG-ABC123"""
        prefix = "VG-"
        while True:
            suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            ref = prefix + suffix
            if not Booking.objects.filter(booking_reference=ref).exists():
                return ref

    def __str__(self):
        return f"Booking {self.id} - {self.customer.name}"

    def nights(self):
        return (self.check_out - self.check_in).days


# ── Dynamic Homepage Content Models ───────────────────────────────────────────

class HeroSlide(models.Model):
    """Dynamic hero slides for homepage"""
    title = models.CharField(max_length=200, help_text='HTML allowed, e.g. Experience <em>Refined</em> Comfort')
    subtitle = models.TextField(max_length=500)
    image = models.ImageField(upload_to='hero/')
    button_text = models.CharField(max_length=50, default='Explore Rooms')
    button_link = models.CharField(max_length=200, default='lodge:rooms',
                                   help_text='Django URL name, e.g. lodge:rooms')
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class AboutSection(models.Model):
    """About section content for the homepage"""
    title = models.CharField(max_length=200, help_text='HTML allowed')
    subtitle = models.CharField(max_length=200, blank=True, default='About Villa Grande')
    description = models.TextField()
    image_main = models.ImageField(upload_to='about/')
    image_accent = models.ImageField(upload_to='about/', blank=True, null=True)
    years_of_excellence = models.PositiveIntegerField(default=15)
    button_text = models.CharField(max_length=50, default='Discover Our Story')
    button_link = models.CharField(max_length=200, default='lodge:about')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Statistic(models.Model):
    """Statistics shown inside the About section"""
    about_section = models.ForeignKey(AboutSection, on_delete=models.CASCADE, related_name='statistics')
    label = models.CharField(max_length=100)
    value = models.PositiveIntegerField()
    suffix = models.CharField(max_length=20, blank=True, help_text='e.g. +, %, K')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Statistics'

    def __str__(self):
        return f"{self.label}: {self.value}{self.suffix}"


class Service(models.Model):
    """Services shown on the homepage services section"""
    ICON_CHOICES = [
        ('fa-hotel', 'Hotel'),
        ('fa-utensils', 'Restaurant'),
        ('fa-spa', 'Spa'),
        ('fa-swimming-pool', 'Pool'),
        ('fa-glass-cheers', 'Events'),
        ('fa-concierge-bell', 'Concierge'),
        ('fa-wifi', 'Wi-Fi'),
        ('fa-dumbbell', 'Gym'),
        ('fa-car', 'Parking'),
        ('fa-shuttle-van', 'Shuttle'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    icon = models.CharField(max_length=50, choices=ICON_CHOICES, default='fa-hotel')
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class ExperienceSection(models.Model):
    """The split experience/video section on the homepage"""
    title = models.CharField(max_length=200, help_text='HTML allowed')
    description = models.TextField()
    video_url = models.URLField(help_text='YouTube or Vimeo embed URL')
    background_image = models.ImageField(upload_to='experience/')
    button_one_text = models.CharField(max_length=50, default='Our Rooms')
    button_one_link = models.CharField(max_length=200, default='lodge:rooms')
    button_two_text = models.CharField(max_length=50, default='Book a Stay')
    button_two_link = models.CharField(max_length=200, default='lodge:booking')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    """Guest testimonials displayed on the homepage"""
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    text = models.TextField(max_length=500)
    image = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    rating = models.PositiveIntegerField(default=5, choices=[(i, i) for i in range(1, 6)])
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.name} — {self.rating}★"


class NewsletterSection(models.Model):
    """Newsletter section text content"""
    title = models.CharField(max_length=200, help_text='HTML allowed')
    subtitle = models.CharField(max_length=200, blank=True)
    placeholder_text = models.CharField(max_length=100, default='Enter your email address')
    button_text = models.CharField(max_length=50, default='Subscribe')
    privacy_link = models.CharField(max_length=200, default='#')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class NewsletterSubscriber(models.Model):
    """Stores newsletter subscriptions"""
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email

class SiteSettings(models.Model):
    """Global site settings – only one instance should exist."""
    site_name = models.CharField(max_length=100, default='Villa Grande')
    tagline = models.CharField(max_length=200, default='Luxury Lodge')
    address = models.TextField(help_text='Full physical address')
    phone = models.CharField(max_length=30)
    email = models.EmailField()
    whatsapp = models.CharField(max_length=30, blank=True, help_text='WhatsApp number')

    # Social media links (optional)
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)

    # Logo – you can upload a custom logo
    logo = models.ImageField(upload_to='site/', blank=True, null=True, help_text='Site logo (optional)')

    # Footer copyright text
    copyright_text = models.CharField(max_length=200, default='© {year} Villa Grande Lodge. All rights reserved.')

    # To enforce a single instance, we override save
    def save(self, *args, **kwargs):
        # If this is not the first instance, delete the old one
        if not self.pk and SiteSettings.objects.exists():
            # Alternatively, you could update the existing record
            existing = SiteSettings.objects.first()
            self.pk = existing.pk
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return self.site_name
    
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.name} - {self.created_at:%Y-%m-%d}"