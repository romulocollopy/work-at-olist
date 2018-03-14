from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from utils.test import AuthUserTestMixin


class CallEventViewTestCase(AuthUserTestMixin, APITestCase):

    def setUp(self):
        self.url = reverse('api:call-event')
        self.auth_user()

    def test_get_not_allowed(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_get_not_authenticated_user_unauthorized(self):
        self.client.logout()
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_not_authenticated_user_unauthorized(self):
        self.client.logout()
        resp = self.client.post(self.url)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_ok(self):
        resp = self.client.post(self.url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
