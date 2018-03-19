from datetime import datetime, timedelta
from django.test import TestCase
from django.urls import reverse
from utils.test import AuthUserTestMixin
from rest_framework import status

class IntegrationTestCase(AuthUserTestMixin, TestCase):

    def setUp(self):
        self.event_url = reverse('api:call-event')
        self.bill_url = reverse('api:call-bill')
        start = datetime(2018, 3, 3, 4, 3, 5)
        end = start + timedelta(seconds=180)
        self.call_start_data = {
            "id": 13,
            "type": "start",
            "timestamp": start.isoformat(),
            "call_id": 2234,
            "source":  "21999888777",
            "destination": "34777888999",
         }

        self.call_end_data = {
            "id": 17,
            "type": "end",
            "timestamp": end.isoformat(),
            "call_id": 2234,
         }
        self.auth_user()

    def test_integration(self):
        self.client.post(self.event_url, self.call_start_data)
        self.client.post(self.event_url, self.call_end_data)

        resp = self.client.get(
            self.bill_url, dict(source="21999888777", month=3, year=2018)
        )

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
