from datetime import datetime, timedelta
from django.test import TestCase
from apps.core.factories import EventFactory
from apps.core.events.call_events import CallStartEvent, CallEndEvent


class EventFactoryTestCase(TestCase):

    def setUp(self):
        start = datetime(2018, 3, 3, 4, 3, 5)
        end = start + timedelta(seconds=180)
        self.call_end_data = {
            "id": 17,
            "type": "end",
            "timestamp": end.isoformat(),
            "call_id": 2234,
         }
        self.call_start_data = {
            "id": 13,
            "type": "start",
            "timestamp": start.isoformat(),
            "call_id": 2234,
            "source":  "21999888777",
            "destination": "34777888999",
         }
        self.factory = EventFactory()

    def test_build_call_start(self):
        event = self.factory.build(**self.call_start_data)
        self.assertIsInstance(event, CallStartEvent)

    def test_build_call_end(self):
        event = self.factory.build(**self.call_end_data)
        self.assertIsInstance(event, CallEndEvent)

    def test_invalid_event(self):
        kwargs = dict(type="eggs")
        with self.assertRaises(ValueError):
            self.factory.build(**kwargs)
