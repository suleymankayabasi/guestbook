from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from datetime import datetime
from .models import User, Entry

class GuestBookEndToEndTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_guestbook_flow(self):
        # Create test users
        user1 = User.objects.create(name='user1', created_date=datetime.now())
        user2 = User.objects.create(name='user2', created_date=datetime.now())

        # Test creating entries
        entry_data = {
            'user': 'user1',
            'subject': 'Test Subject 1',
            'message': 'Test message 1'
        }
        create_entry_url = reverse('guestbook:create-entry')  # Adjust URL name according to your project

        response = self.client.post(create_entry_url, entry_data, format='json')
        self.assertEqual(response.status_code, 201)

        # Test retrieving entries
        get_entries_url = reverse('guestbook:entry-list')  # Adjust URL name according to your project
        response = self.client.get(get_entries_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['entries']), 1)  # Assuming one entry was created

        # Test retrieving users' data
        get_users_data_url = reverse('guestbook:get-users-data')  # Adjust URL name according to your project
        response = self.client.get(get_users_data_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['users']), 2)  # Assuming two users exist

        # Additional assertions based on your specific requirements
        # Example: Check if the last_entry format is as expected

        last_entry_format = response.data['users'][0]['last_entry']
        self.assertIn('|', last_entry_format)  # Check if format "subject | message" is followed

