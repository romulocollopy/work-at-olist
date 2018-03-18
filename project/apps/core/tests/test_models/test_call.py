import datetime, pytz
import mock
from django.test import TestCase
from django.utils import timezone
from model_mommy import mommy
from apps.core.models import Call as CallModel


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
