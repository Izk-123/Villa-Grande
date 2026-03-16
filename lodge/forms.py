from django import forms
from .models import Booking, Customer, Room
from django.core.exceptions import ValidationError
from datetime import date

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

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = '__all__'