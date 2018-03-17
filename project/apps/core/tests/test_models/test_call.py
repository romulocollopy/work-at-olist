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
        self.assertEqual(call.duration, datetime.timedelta(seconds=240))
        self.assertEqual(call.price, 22.50)

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
