import mock
from django.urls import reverse
from django.http.request import QueryDict
from rest_framework.test import APITestCase
from rest_framework import status
from utils.test import AuthUserTestMixin
from api.views import CallEventView


class CallEventViewTestCase(AuthUserTestMixin, APITestCase):

    def setUp(self):
        self.get_serializer = mock.Mock()
        self.get_use_case = mock.Mock()
        self.serializer_patcher = mock.patch(
            'api.views.call_event_view.CallEventView.get_serializer',
            new_callable=self.get_serializer,
        )
        self.use_case_patcher = mock.patch(
            'api.views.call_event_view.CallEventView.get_use_case',
            new_callable=self.get_use_case,
        )
        self.serializer_patcher.start()
        self.use_case_patcher.start()
        self.url = reverse('api:call-event')
        self.data = dict(spam='eggs')
        serializer = self.get_serializer()
        serializer.return_value.data = self.data
        self.auth_user()

    def tearDown(self):
        self.serializer_patcher.stop()
        self.use_case_patcher.stop()

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
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_post_calls_serializer(self):
        self.client.post(self.url, self.data)
        qd = QueryDict(mutable=True)
        qd.update(self.data)
        serializer = self.get_serializer()
        serializer.assert_called_once_with(qd)
        serializer().is_valid.assert_called_once_with()

    def test_post_calls_get_use_case_when_serializer_is_valid(self):
        self.client.post(self.url, self.data)
        self.get_use_case.assert_called_once_with()
        use_case = self.get_use_case()
        use_case().execute.assert_called_once_with(**self.data)

    def test_get_serializer(self):
        view = CallEventView()
        view.serializer_class = mock.Mock()
        self.serializer_patcher.temp_original(view, self.data)
        view.serializer_class.assert_called_once_with(data=self.data)

    def test_get_use_case(self):
        view = CallEventView()
        view.use_case_class = mock.Mock()
        self.use_case_patcher.temp_original(view)
        view.use_case_class.assert_called_once_with()
