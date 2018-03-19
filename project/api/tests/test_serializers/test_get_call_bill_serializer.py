import mock
from django.test import TestCase
from django.utils import timezone
from freezegun import freeze_time
from api.serializers import GetCallBillSerializer


class GetBillSerializerTestCase(TestCase):

    def setUp(self):
        self.data = dict(
            source=21999888777,
            month=3,
            year=2018,
        )
        self.serializer = GetCallBillSerializer()

    def test_get_period_with_args(self):
        period = self.serializer._get_period('123', '321')
        self.assertEqual(period, (123, 321))

    def test_get_period_with_month_eq_1(self):
        year = timezone.now().year
        period = self.serializer._get_period('1', None)
        self.assertEqual(period, (1, year))

    def test_get_period_with_month_gt_1(self):
        year = timezone.now().year
        period = self.serializer._get_period('2', None)
        self.assertEqual(period, (2, year))

    @freeze_time('2018-03-01')
    def test_get_period_wo_args(self):
        period = self.serializer._get_period(None, None)
        self.assertEqual(period, (2, 2018))

    @freeze_time('2018-01-01')
    def test_get_period_wo_args_in_january(self):
        period = self.serializer._get_period(None, None)
        self.assertEqual(period, (12, 2017))

    @freeze_time('2018-01-01')
    def test_get_period_with_year_keeps_month(self):
        period = self.serializer._get_period(None, 2013)
        self.assertEqual(period, (1, 2013))

    @mock.patch.object(GetCallBillSerializer, '_get_period')
    def test_validations(self, _get_period):
        _get_period.return_value = 1, 2
        serializer = GetCallBillSerializer(data=self.data)
        serializer.is_valid()
        _get_period.assert_called_once_with(3, 2018)

    @mock.patch.object(GetCallBillSerializer, '_get_period')
    def test_validate(self, _get_period):
        _get_period.return_value = 1, 2
        serializer = GetCallBillSerializer(data=self.data)
        data = serializer.validate(self.data)
        self.assertEqual(
            data, dict(source=21999888777, month=1, year=2)
        )
