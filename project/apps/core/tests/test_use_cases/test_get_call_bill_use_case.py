import mock
from django.test import TestCase
from apps.core.use_cases import GetCallBillUseCase


class GetCallBillUseCaseTestCase(TestCase):

    def setUp(self):
        self.model = mock.Mock()
        self.use_case = GetCallBillUseCase(model=self.model)
        self.data = dict(
            source='AAXXXXXXXXX',
            month=3,
            year=2018,
        )
        self.model.objects.month_bill.return_value = []

    def test_execute(self):
        self.use_case.execute(**self.data)
        data = {k: v for k, v in self.data.items()}
        self.model.objects.month_bill.assert_called_once_with(
            data.pop('source'), **data
        )
