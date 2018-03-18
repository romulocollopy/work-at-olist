import datetime
import pytz
import mock
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from model_mommy import mommy
from freezegun import freeze_time
from apps.core.models import Call as CallModel
from apps.core.models.call import _get_period


class CallModelTestCase(TestCase):

    def setUp(self):
        start = timezone.make_aware(
            datetime.datetime(2018, 1, 1, 6, 0, 5, 34), timezone=pytz.UTC
        )
        end = start + timezone.timedelta(seconds=240)
        self._load_start_event(start)
        self._load_end_event(end)

    def test_create(self):
        CALL_ID = 72
        mommy.make(CallModel, id=CALL_ID)
        call = CallModel.objects.get()
        self.assertEqual(call.id, CALL_ID)

    def test_handle_start(self):
        CallModel.handle_start(self.call_start_event)
        call = CallModel.objects.get(id=self.call_end_event.call_id)
        self.assertEqual(call.start_timestamp, self.call_start_event.timestamp)
        self.assertEqual(call.source, self.call_start_event.source)
        self.assertEqual(call.destination, self.call_start_event.destination)

    def test_handle_start_calls_pricing_if_has_end_timestamp(self):
        CallModel.pricing_service = mock.Mock()
        CallModel.pricing_service.get_price.return_value = 22.50
        mommy.make(
            CallModel,
            id=self.call_end_event.call_id,
            end_timestamp=self.call_end_event.timestamp,
        )
        CallModel.handle_start(self.call_start_event)
        call = CallModel.objects.get(id=self.call_end_event.call_id)
        self.assertEqual(
            self.call_end_event.timestamp - self.call_start_event.timestamp,
            call.duration
        )
        self.assertEqual(22.50, call.price)

    def test_handle_end(self):
        CallModel.pricing_service = mock.Mock()
        CallModel.pricing_service.get_price.return_value = 22.50
        mommy.make(
            CallModel,
            id=self.call_end_event.call_id,
            start_timestamp=self.call_start_event.timestamp,
        )
        CallModel.handle_end(self.call_end_event)
        call = CallModel.objects.get(id=self.call_end_event.call_id)
        CallModel.pricing_service.get_price.assert_called_once_with(call)
        self.assertEqual(call.duration, datetime.timedelta(seconds=240))
        self.assertEqual(call.price, 22.50)

    def test_handle_end_does_not_get_price_without_start(self):
        CallModel.pricing_service = mock.Mock()
        mommy.make(
            CallModel,
            id=self.call_end_event.call_id,
            start_timestamp=None,
        )
        CallModel.handle_end(self.call_end_event)
        call = CallModel.objects.get(id=self.call_end_event.call_id)
        self.assertEqual(CallModel.pricing_service.get_price.call_count, 0)
        self.assertEqual(call.duration, None)
        self.assertEqual(call.price, None)

    def test_validate_start_gt_end(self):
        start_timestamp = self.call_start_event.timestamp
        end_timestamp = start_timestamp - datetime.timedelta(seconds=300)
        call = CallModel(
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
        )
        with self.assertRaises(ValidationError):
            call.clean()

    def test_validate_negative_duration(self):
        start_timestamp = self.call_start_event.timestamp
        end_timestamp = start_timestamp - datetime.timedelta(seconds=300)
        call = CallModel(
            duration=end_timestamp - start_timestamp,
        )
        with self.assertRaises(ValidationError):
            call.clean()

    def _load_start_event(self, start):
        call_start_event = mock.Mock()
        call_start_event.call_id = 722
        call_start_event.timestamp = start
        call_start_event.source = '21999888777'
        call_start_event.destination = '21777888999'
        self.call_start_event = call_start_event

    def _load_end_event(self, end):
        call_end_event = mock.Mock()
        call_end_event.call_id = 722
        call_end_event.timestamp = end
        self.call_end_event = call_end_event


class CallManagerTestCase(TestCase):

    def setUp(self):
        mommy.make(
            CallModel, source='AAXXXXXXXXX', _quantity=8,
            start_timestamp='2018-01-01',
            end_timestamp=timezone.datetime(2018, 2, 5))

        mommy.make(
            CallModel, source='AAXXXXXXXXX', _quantity=6,
            start_timestamp='2018-01-01',
            end_timestamp=timezone.datetime(2018, 1, 6)
        )

        mommy.make(
            CallModel, source='BBXXXXXXXXX', _quantity=3,
            start_timestamp='2018-01-01',
            end_timestamp=timezone.datetime(2018, 2, 5)
        )

    def test_month_bill_requires_source(self):
        with self.assertRaises(TypeError):
            CallModel.objects.month_bill()

    def test_month_bill_gets_calls_from_source(self):
        bill = CallModel.objects.month_bill('AAXXXXXXXXX')
        list(map(lambda b: self.assertEqual('AAXXXXXXXXX', b.source), bill))

    def test_month_bill_gets_calls_from_month(self):
        closed_month = timezone.datetime(2018, 2, 4)
        bill = CallModel.objects.month_bill(
            'BBXXXXXXXXX',
            month=closed_month.month,
            year=closed_month.year,
        )
        list(map(
            lambda b: self.assertEqual(
                (closed_month.year, closed_month.month),
                (b.end_timestamp.year, b.end_timestamp.month)
            ),
            bill)
        )
        self.assertEqual(bill.count(), 3)

    def test_get_period_with_args(self):
        period = _get_period('123', '321')
        self.assertEqual(period, (123, 321))

    def test_get_period_with_month_eq_1(self):
        year = timezone.now().year
        period = _get_period('1', None)
        self.assertEqual(period, (1, year))

    def test_get_period_with_month_gt_1(self):
        year = timezone.now().year
        period = _get_period('2', None)
        self.assertEqual(period, (2, year))

    @freeze_time('2018-03-01')
    def test_get_period_wo_args(self):
        period = _get_period(None, None)
        self.assertEqual(period, (2, 2018))

    @freeze_time('2018-01-01')
    def test_get_period_wo_args_in_january(self):
        period = _get_period(None, None)
        self.assertEqual(period, (12, 2017))

    @freeze_time('2018-01-01')
    def test_get_period_with_year_keeps_month(self):
        period = _get_period(None, 2013)
        self.assertEqual(period, (1, 2013))
