import re

from django import forms

from .models import Event, Registration


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'category', 'date', 'venue', 'description', 'image_label', 'is_active']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class RegistrationForm(forms.Form):
    full_name = forms.CharField(
        min_length=3,
        max_length=200,
        widget=forms.TextInput(attrs={'placeholder': 'Your name'}),
    )
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'you@college.edu'}))
    phone = forms.CharField(
        min_length=10,
        max_length=15,
        widget=forms.TextInput(attrs={'placeholder': '10-digit number'}),
    )
    department = forms.ChoiceField(
        choices=[
            ('', 'Select department'),
            ('CSD', 'Computer Science & Design'),
            ('CSE', 'Computer Science'),
            ('IT', 'Information Technology'),
            ('ECE', 'Electronics'),
            ('ME', 'Mechanical'),
            ('CE', 'Civil'),
        ],
    )
    event = forms.ChoiceField(choices=[('', 'Choose an event')])
    terms_accepted = forms.BooleanField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        event_choices = [('', 'Choose an event')]
        event_choices.extend(
            (event.title, event.title)
            for event in Event.objects.filter(is_active=True).order_by('title')
        )
        self.fields['event'].choices = event_choices

    def clean_full_name(self):
        full_name = self.cleaned_data['full_name'].strip()
        if not re.fullmatch(r"^[A-Za-z ]{3,}$", full_name):
            raise forms.ValidationError('Please enter a valid name.')
        return full_name

    def clean_phone(self):
        phone = self.cleaned_data['phone'].strip()
        if not re.fullmatch(r'^\d{10}$', phone):
            raise forms.ValidationError('Please enter a valid 10-digit phone number.')
        return phone

    def clean_event(self):
        event_title = self.cleaned_data['event']
        if not event_title:
            raise forms.ValidationError('Please choose an event.')
        try:
            return Event.objects.get(title=event_title, is_active=True)
        except Event.DoesNotExist:
            raise forms.ValidationError('Please choose a valid event.')

    def save(self):
        event = self.cleaned_data['event']
        return Registration.objects.create(
            event=event,
            full_name=self.cleaned_data['full_name'].strip(),
            email=self.cleaned_data['email'].strip(),
            phone=self.cleaned_data['phone'].strip(),
            department=self.cleaned_data['department'],
            terms_accepted=True,
        )
