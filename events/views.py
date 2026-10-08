from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import EventForm, RegistrationForm
from .models import Event, Registration


def ensure_seed_data():
    events = [
        {
            'title': 'CodeSprint 2026',
            'category': 'technical',
            'date': '2026-10-18',
            'venue': 'Computer Lab',
            'description': 'A coding challenge for students who enjoy problem solving and programming.',
            'image_label': 'TECH',
        },
        {
            'title': 'Campus Carnival',
            'category': 'cultural',
            'date': '2026-10-25',
            'venue': 'Main Ground',
            'description': 'Music, dance, food and performances by students from across the college.',
            'image_label': 'CULTURE',
        },
        {
            'title': 'Inter College Cup',
            'category': 'sports',
            'date': '2026-11-02',
            'venue': 'Sports Ground',
            'description': 'Bring your team, represent your department and compete for the cup.',
            'image_label': 'SPORTS',
        },
        {
            'title': 'RoboWars',
            'category': 'technical',
            'date': '2026-11-10',
            'venue': 'Innovation Lab',
            'description': 'Build your robot, test your design and take it into the arena.',
            'image_label': 'ROBOTICS',
        },
        {
            'title': 'Research Symposium',
            'category': 'academic',
            'date': '2026-11-15',
            'venue': 'Seminar Hall',
            'description': 'Share your ideas, projects and research with students and faculty.',
            'image_label': 'RESEARCH',
        },
        {
            'title': 'Battle of Bands',
            'category': 'cultural',
            'date': '2026-11-20',
            'venue': 'College Auditorium',
            'description': 'Grab your instruments and compete with the best campus bands.',
            'image_label': 'MUSIC',
        },
    ]

    if Event.objects.count() == 0:
        Event.objects.bulk_create([
            Event(**event) for event in events
        ])


def home(request):
    ensure_seed_data()
    events = Event.objects.filter(is_active=True).order_by('date')
    form = RegistrationForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Registration successful! Your spot has been saved for the event.')
        return redirect('home')

    return render(request, 'events/home.html', {
        'events': events,
        'form': form,
    })


def event_list(request):
    selected_category = request.GET.get('category', 'all')
    events = Event.objects.filter(is_active=True).order_by('date')
    if selected_category != 'all':
        events = events.filter(category=selected_category)

    total_events = Event.objects.filter(is_active=True).count()
    total_registrations = Registration.objects.count()
    category_breakdown = {
        key: Event.objects.filter(is_active=True, category=key).count()
        for key, _ in Event.CATEGORY_CHOICES
    }

    return render(request, 'events/event_list.html', {
        'events': events,
        'selected_category': selected_category,
        'total_events': total_events,
        'total_registrations': total_registrations,
        'category_breakdown': category_breakdown,
    })


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    registrations = Registration.objects.filter(event=event).order_by('-created_at')
    return render(request, 'events/event_detail.html', {'event': event, 'registrations': registrations})


def registrations_list(request):
    registrations = Registration.objects.select_related('event').order_by('-created_at')
    return render(request, 'events/registration_list.html', {'registrations': registrations})


def registration_delete(request, pk):
    registration = get_object_or_404(Registration, pk=pk)
    if request.method == 'POST':
        registration.delete()
        messages.success(request, 'Participant removed successfully.')
        return redirect('registrations_list')
    return render(request, 'events/registration_confirm_delete.html', {'registration': registration})


def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event created successfully.')
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'events/event_form.html', {'form': form, 'title': 'Create Event'})


def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event updated successfully.')
            return redirect('event_detail', pk=event.pk)
    else:
        form = EventForm(instance=event)
    return render(request, 'events/event_form.html', {'form': form, 'title': 'Update Event'})


def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted successfully.')
        return redirect('event_list')
    return render(request, 'events/event_confirm_delete.html', {'event': event})
