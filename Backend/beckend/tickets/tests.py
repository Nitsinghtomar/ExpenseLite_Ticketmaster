# /backend/tickets/tests.py (extended with user registration and login tests)
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Ticket, Status
from rest_framework_simplejwt.tokens import RefreshToken

class UserAPITestCase(APITestCase):
    def test_user_registration(self):
        response = self.client.post('/api/users/', {'username': 'newuser', 'password': 'newpass'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'newuser')

    def test_user_login(self):
        User.objects.create_user(username='testuser', password='testpass')
        response = self.client.post('/api/users/login/', {'username': 'testuser', 'password': 'testpass'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

class TicketAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_create_ticket(self):
        response = self.client.post('/api/tickets/', {'title': 'Test Ticket', 'description': 'Test Description'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Ticket.objects.count(), 1)
        self.assertEqual(Ticket.objects.get().title, 'Test Ticket')

    def test_update_ticket(self):
        ticket = Ticket.objects.create(title='Test Ticket', description='Test Description', user=self.user)
        response = self.client.put(f'/api/tickets/{ticket.id}/', {'title': 'Updated Ticket', 'description': 'Updated Description'})
        self.assertEqual(response.status_code, 200)
        ticket.refresh_from_db()
        self.assertEqual(ticket.title, 'Updated Ticket')

    def test_delete_ticket(self):
        ticket = Ticket.objects.create(title='Test Ticket', description='Test Description', user=self.user)
        response = self.client.delete(f'/api/tickets/{ticket.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Ticket.objects.count(), 0)

class ReportAPITestCase(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(username='adminuser', password='adminpass')
        self.user = User.objects.create_user(username='testuser', password='testpass')
        refresh = RefreshToken.for_user(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_report_open_vs_closed_tickets(self):
        Ticket.objects.create(title='Open Ticket', description='Test Description', status='open', user=self.user)
        Ticket.objects.create(title='Closed Ticket', description='Test Description', status='closed', user=self.user)
        response = self.client.get('/api/reports/open-vs-closed/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_report_average_resolution_time(self):
        ticket = Ticket.objects.create(title='Closed Ticket', description='Test Description', status='closed', user=self.user)
        Status.objects.create(ticket=ticket, status='closed')
        response = self.client.get('/api/reports/average-resolution-time/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('avg_resolution_time', response.data)
