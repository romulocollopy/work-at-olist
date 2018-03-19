import mock
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.http import QueryDict
from utils.test import AuthUserTestMixin


class BillViewTestCase(AuthUserTestMixin, APITestCase):

    def setUp(self):
        self.url = reverse('api:call-bill')
        self.get_serializer = mock.Mock()
        self.get_use_case = mock.Mock()
        self.serializer_patcher = mock.patch(
            'api.views.call_bill_view.CallBillView.get_serializer',
            new_callable=self.get_serializer,
        )
        self.use_case_patcher = mock.patch(
            'api.views.call_bill_view.CallBillView.get_use_case',
            new_callable=self.get_use_case,
        )
        self.serializer_patcher.start()
        self.use_case_patcher.start()
        self.get_use_case()().execute.return_value = dict(foo='bar')
        self.data = dict(spam='eggs')
        self.get_serializer().return_value.data = self.data
        self.auth_user()

    def tearDown(self):
        self.serializer_patcher.stop()
        self.use_case_patcher.stop()

    def test_get_calls_serializer(self):
        qd = QueryDict(mutable=True)
        qd.update(self.data)
        self.client.get(self.url, self.data)
        self.get_serializer().assert_called_once_with(qd)

    def test_get_ok_when_serializer_is_valid(self):
        self.get_serializer().is_valid.return_value = True
        resp = self.client.get(self.url, self.data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_get_bad_request_when_serializer_is_not_valid(self):
        self.get_serializer()().is_valid.return_value = False
        self.get_serializer()().errors = self.data
        resp = self.client.get(self.url, self.data)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_use_case_called(self):
        self.client.get(self.url, self.data)
        self.get_use_case()().execute.assert_called_once_with(**self.data)
