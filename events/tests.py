from django.test import TestCase
from django.urls import reverse

from .models import Event, Registration


class EventEaseViewsTests(TestCase):
    def setUp(self):
        self.event = Event.objects.create(
            title='CodeSprint 2026',
            category='technical',
            date='2026-10-18',
            venue='Computer Lab',
            description='Coding challenge for problem solvers.',
            image_label='TECH',
        )

    def test_home_page_displays_events(self):
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'CodeSprint 2026')
        self.assertContains(response, 'Upcoming events')

    def test_registration_can_be_saved(self):
        response = self.client.post(
            reverse('home'),
            {
                'full_name': 'Aarav Sharma',
                'email': 'aarav@college.edu',
                'phone': '9876543210',
                'department': 'CSE',
                'event': self.event.title,
                'terms_accepted': 'on',
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Registration.objects.filter(email='aarav@college.edu').exists())
        self.assertContains(response, 'Registration successful')

    def test_invalid_registration_is_not_saved_and_shows_errors(self):
        response = self.client.post(
            reverse('home'),
            {
                'full_name': 'Aarav Sharma',
                'email': 'aarav@college.edu',
                'phone': '9876543210',
                'department': 'CSE',
                'event': self.event.title,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Registration.objects.filter(email='aarav@college.edu').exists())
        self.assertContains(response, 'This field is required.')

    def test_event_list_and_create_work(self):
        create_response = self.client.post(
            reverse('event_create'),
            {
                'title': 'AI Expo',
                'category': 'technical',
                'date': '2026-12-05',
                'venue': 'Innovation Hub',
                'description': 'Students showcase AI projects and prototypes.',
                'image_label': 'AI',
                'is_active': 'on',
            },
        )

        self.assertEqual(create_response.status_code, 302)
        self.assertTrue(Event.objects.filter(title='AI Expo').exists())

        list_response = self.client.get(reverse('event_list'))
        self.assertEqual(list_response.status_code, 200)
        self.assertContains(list_response, 'AI Expo')

    def test_registered_participants_are_visible(self):
        Registration.objects.create(
            event=self.event,
            full_name='Priya Rao',
            email='priya@college.edu',
            phone='9988776655',
            department='CSE',
            terms_accepted=True,
        )

        response = self.client.get(reverse('registrations_list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Priya Rao')
        self.assertContains(response, 'CodeSprint 2026')

    def test_participants_can_be_deleted_and_events_can_be_filtered(self):
        registration = Registration.objects.create(
            event=self.event,
            full_name='Rohit Nair',
            email='rohit@college.edu',
            phone='8899776655',
            department='IT',
            terms_accepted=True,
        )

        delete_response = self.client.post(reverse('registration_delete', args=[registration.pk]))
        self.assertEqual(delete_response.status_code, 302)
        self.assertFalse(Registration.objects.filter(pk=registration.pk).exists())

        festival = Event.objects.create(
            title='Cultural Fest',
            category='cultural',
            date='2026-11-12',
            venue='Open Stage',
            description='Annual cultural celebration.',
            image_label='FEST',
        )

        response = self.client.get(reverse('event_list') + '?category=cultural')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Cultural Fest')
