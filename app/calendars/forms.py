from django import forms
from .models import Event, Calendar


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ("creator", "calendar", "rule", "end_recurring_period", "color_event")