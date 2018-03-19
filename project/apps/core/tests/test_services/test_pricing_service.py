import datetime
import mock
from decimal import Decimal
from django.test import TestCase
from apps.core.services import PricingService


class PricingServiceTestCase(TestCase):

    def setUp(self):
        self.call = mock.Mock()
        self.call.duration = datetime.timedelta(seconds=(48 * 60 * 60))
        self.call.start_timestamp = datetime.datetime(2017, 12, 31, 15, 35, 22)
        self.service = PricingService()

    @mock.patch.object(PricingService, '_get_entire_days_value')
    @mock.patch.object(PricingService, '_get_normal_minutes_value')
    @mock.patch.object(PricingService, '_get_reduced_minutes_value')
    def test_get_price(self, reduced_value, normal_value, entire_days):
        reduced_value.return_value = Decimal('0.5')
        normal_value.return_value = Decimal('17.8')
        entire_days.return_value = Decimal('172.80')

        price = self.service.get_price(self.call)

        reduced_value.assert_called_once_with(self.call)
        normal_value.assert_called_once_with(self.call)

        self.assertEqual(
            price,
            self.service.standing_charge +
            reduced_value() +
            normal_value() +
            entire_days()
        )

    @mock.patch.object(PricingService, '_get_normal_minutes')
    def test_get_normal_minutes_value(self, normal_minutes):
        normal_minutes.return_value = 13
        value = self.service._get_normal_minutes_value(self.call)
        normal_minutes.assert_called_once_with(self.call)
        self.assertEqual(value, 13 * self.service.normal_minute)

    @mock.patch.object(PricingService, '_get_reduced_minutes')
    def test_get_reduced_minutes_value(self, reduced_minutes):
        reduced_minutes.return_value = 27
        value = self.service._get_reduced_minutes_value(self.call)
        reduced_minutes.assert_called_once_with(self.call)
        self.assertEqual(value, 27 * self.service.reduced_minute)

    def test_get_normal_minutes(self):
        self.call.start_timestamp = datetime.datetime(2017, 12, 31, 15, 35, 22)
        self.call.duration = datetime.timedelta(seconds=120 * 60)
        minutes = self.service._get_normal_minutes(self.call)
        self.assertEquals(minutes, 120)

    def test_get_normal_minutes_overnight(self):
        self.call.start_timestamp = datetime.datetime(2017, 12, 31, 18, 00, 00)
        self.call.duration = datetime.timedelta(seconds=13 * 60 * 60)
        minutes = self.service._get_normal_minutes(self.call)
        self.assertEquals(minutes, 5 * 60)

    def test_get_normal_minutes_past_mindight(self):
        self.call.start_timestamp = datetime.datetime(2017, 12, 31, 18, 00, 00)
        self.call.duration = datetime.timedelta(seconds=8 * 60 * 60)
        minutes = self.service._get_normal_minutes(self.call)
        self.assertEquals(minutes, 4 * 60)

    def test_get_normal_minutes_starting_early(self):
        self.call.start_timestamp = datetime.datetime(2017, 12, 31, 3, 00, 00)
        self.call.duration = datetime.timedelta(seconds=5 * 60 * 60)
        minutes = self.service._get_normal_minutes(self.call)
        self.assertEquals(minutes, 2 * 60)

    def test_get_normal_minutes_starting_early_finishing_late(self):
        self.call.start_timestamp = datetime.datetime(2017, 12, 31, 5, 00, 00)
        self.call.duration = datetime.timedelta(seconds=18 * 60 * 60)
        minutes = self.service._get_normal_minutes(self.call)
        self.assertEquals(minutes, 16 * 60)

    def test_get_normal_minutes_short_call(self):
        self.call.start_timestamp = datetime.datetime(2017, 12, 31, 10, 00, 00)
        self.call.duration = datetime.timedelta(seconds=0.5 * 60 * 60)
        minutes = self.service._get_normal_minutes(self.call)
        self.assertEquals(minutes, 0.5 * 60)

    def test_docs_example(self):
        self.call.start_timestamp = datetime.datetime(2017, 12, 31, 21, 57, 13)
        self.call.duration = datetime.timedelta(seconds=13 * 60 + 43)
        minutes = self.service._get_normal_minutes(self.call)
        self.assertEquals(minutes, 2)

    def test_get_entire_days_value(self):
        value = self.service._get_entire_days_value(self.call)
        self.assertEqual(value, Decimal('172.80'))

    def test_get_reduced_minutes(self):
        """ this first implementation will always return 0 """
        minutes = self.service._get_reduced_minutes(self.call)
        self.assertEqual(minutes, 0)
