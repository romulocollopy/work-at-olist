import mock
from django.urls import reverse
from django.http.request import QueryDict
from rest_framework.test import APITestCase
from rest_framework import status
from utils.test import AuthUserTestMixin


class CallEventViewTestCase(AuthUserTestMixin, APITestCase):

    def setUp(self):
        self.serializer_class = mock.Mock()
        self.patcher = mock.patch(
            'api.views.call_event_view.CallEventView.serializer_class',
            new_callable=self.serializer_class,
        )
        self.patcher.start()
        self.url = reverse('api:call-event')
        self.data = dict(spam='eggs')
        self.auth_user()

    def tearDown(self):
        self.patcher.stop()

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

    def test_post_calls_serializer(self):
        self.client.post(self.url, self.data)
        qd = QueryDict(mutable=True)
        qd.update(self.data)
        self.serializer_class().assert_called_once_with(data=qd)
        self.serializer_class()().is_valid.assert_called_once_with()
