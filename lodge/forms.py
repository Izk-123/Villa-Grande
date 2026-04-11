from django import forms
from .models import Booking, ContactMessage, Customer, Room, NewsletterSubscriber
from django.core.exceptions import ValidationError
from datetime import date, datetime, timedelta
import re

# Keep the original BookingForm for backward compatibility
class BookingForm(forms.Form):
    name = forms.CharField(max_length=100, label='Full Name')
    phone = forms.CharField(max_length=20, label='Phone Number')
    email = forms.EmailField(required=False, label='Email (optional)')
    check_in = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    check_out = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    guests = forms.IntegerField(min_value=1, max_value=10, initial=2)
    room = forms.ModelChoiceField(queryset=Room.objects.filter(is_active=True), empty_label="Select a room")

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')
        room = cleaned_data.get('room')

        if check_in and check_out and check_in >= check_out:
            raise ValidationError('Check-out must be after check-in.')

        if check_in and check_in < date.today():
            raise ValidationError('Check-in cannot be in the past.')

        # Check availability
        if room and check_in and check_out:
            overlapping = Booking.objects.filter(
                room=room,
                status__in=['PENDING', 'CONFIRMED'],
                check_in__lt=check_out,
                check_out__gt=check_in
            )
            if overlapping.exists():
                raise ValidationError('This room is not available for the selected dates.')
        return cleaned_data


class DatePickerInput(forms.DateInput):
    """Custom date picker with min/max attributes"""
    def __init__(self, attrs=None):
        default_attrs = {
            'type': 'date',
            'class': 'modern-date-input',
            'min': date.today().isoformat(),
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)


class StyledModelChoiceField(forms.ModelChoiceField):
    """Custom model choice field with styled widget"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget.attrs.update({
            'class': 'modern-select',
            'data-placeholder': 'Select a room'
        })


class ModernBookingForm(forms.Form):
    """Enhanced booking form with modern styling"""
    
    # Personal Information Section
    name = forms.CharField(
        max_length=100,
        label='Full Name',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your full name',
            'required': 'required'
        })
    )
    
    phone = forms.CharField(
        max_length=20,
        label='Phone Number',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+265 888 000 000',
            'required': 'required'
        })
    )
    
    email = forms.EmailField(
        required=False,
        label='Email Address',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your@email.com'
        })
    )
    
    # Stay Details Section
    check_in = forms.DateField(
        label='Check In',
        required=True,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'required': 'required'
        })
    )
    
    check_out = forms.DateField(
        label='Check Out',
        required=True,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'required': 'required'
        })
    )
    
    guests = forms.IntegerField(
        min_value=1,
        max_value=10,
        initial=2,
        label='Number of Guests',
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '1',
            'max': '10',
            'required': 'required'
        })
    )
    
    # Room Selection
    room = forms.ModelChoiceField(
        queryset=Room.objects.filter(is_active=True),
        empty_label="Select a room",
        label='Choose Your Room',
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'required': 'required'
        })
    )
    
    # Special Requests
    special_requests = forms.CharField(
        required=False,
        label='Special Requests',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Any special requirements?',
            'rows': 3
        })
    )
    
    # Preferences
    PREFERENCE_CHOICES = [
        ('non_smoking', 'Non-Smoking Room'),
        ('extra_pillows', 'Extra Pillows'),
        ('late_checkout', 'Late Checkout (if available)'),
        ('early_checkin', 'Early Check-in (if available)'),
    ]
    
    preferences = forms.MultipleChoiceField(
        choices=PREFERENCE_CHOICES,
        required=False,
        label='Additional Preferences',
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'preferences-checkbox'
        })
    )
    
    HEAR_ABOUT_CHOICES = [
        ('', 'Select an option'),
        ('google', 'Google Search'),
        ('social', 'Social Media'),
        ('friend', 'Friend/Family'),
        ('previous', 'Previous Guest'),
        ('other', 'Other'),
    ]
    
    hear_about = forms.ChoiceField(
        choices=HEAR_ABOUT_CHOICES,
        required=False,
        label='How did you hear about us?',
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    # Terms Agreement
    agree_terms = forms.BooleanField(
        required=True,
        label='I agree to the terms and conditions',
        widget=forms.CheckboxInput(attrs={
            'class': 'terms-checkbox',
            'required': 'required'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set initial dates
        today = date.today()
        tomorrow = today + timedelta(days=1)
        
        self.fields['check_in'].initial = today
        self.fields['check_out'].initial = tomorrow
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            # Remove common separators
            cleaned = re.sub(r'[\s\-\(\)\+]', '', phone)
            if not cleaned.isdigit() or len(cleaned) < 9:
                raise ValidationError('Please enter a valid phone number')
        return phone
    
    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')
        room = cleaned_data.get('room')
        
        if check_in and check_out:
            if check_in >= check_out:
                raise ValidationError('Check-out must be after check-in.')
            
            if check_in < date.today():
                raise ValidationError('Check-in cannot be in the past.')
            
            # Calculate nights
            nights = (check_out - check_in).days
            if nights > 30:
                raise ValidationError('Maximum stay is 30 nights.')
        
        # Check availability
        if room and check_in and check_out:
            overlapping = Booking.objects.filter(
                room=room,
                status__in=['PENDING', 'CONFIRMED'],
                check_in__lt=check_out,
                check_out__gt=check_in
            )
            if overlapping.exists():
                raise ValidationError('This room is not available for the selected dates.')
        
        return cleaned_data


class QuickBookingForm(forms.Form):
    """Simplified form for the booking bar"""
    check_in = forms.DateField(
        widget=DatePickerInput(attrs={
            'class': 'quick-date-input',
            'id': 'quick_check_in'
        })
    )
    check_out = forms.DateField(
        widget=DatePickerInput(attrs={
            'class': 'quick-date-input',
            'id': 'quick_check_out'
        })
    )
    guests = forms.IntegerField(
        min_value=1,
        max_value=10,
        initial=2,
        widget=forms.NumberInput(attrs={
            'class': 'quick-number-input',
            'min': '1',
            'max': '10',
            'id': 'quick_guests'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        today = date.today()
        tomorrow = today + timedelta(days=1)
        self.fields['check_in'].initial = today
        self.fields['check_out'].initial = tomorrow


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }


class NewsletterForm(forms.ModelForm):
    """Newsletter subscription form"""
    class Meta:
        model = NewsletterSubscriber
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'newsletter-input',
                'placeholder': 'Enter your email address',
                'aria-label': 'Email address'
            })
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if NewsletterSubscriber.objects.filter(email=email, is_active=True).exists():
            raise ValidationError('This email is already subscribed.')
        return email

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5, 'class': 'form-control', 'placeholder': 'Your Message'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Phone (optional)'}),
        }
        
class BookingStatusForm(forms.Form):
    booking_reference = forms.CharField(
        label="Booking ID",
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g. VG-ABC123',
            'aria-label': 'Booking ID'
        })
    )