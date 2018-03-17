import mock
from datetime import datetime, timedelta
from django.test import TestCase
from apps.core.events import CallStartEvent, CallEndEvent


class CallStartEventTestCase(TestCase):

    def setUp(self):
        start = datetime(2018, 3, 3, 4, 3, 5)
        self.call_start_data = {
            "id": 13,
            "type": "start",
            "timestamp": start.isoformat(),
            "call_id": 2234,
            "source":  "21999888777",
            "destination": "34777888999",
         }

    def test_instantiate_call_start(self):
        event = CallStartEvent(**self.call_start_data)
        self.assertIsInstance(event, CallStartEvent)

    def test_process(self):
        event = CallStartEvent(**self.call_start_data)
        event.model = mock.Mock()
        event.process()
        event.model.handle_start.assert_called_once_with(event)


class CallEndEventTestCase(TestCase):

    def setUp(self):
        start = datetime(2018, 3, 3, 4, 3, 5)
        end = start + timedelta(seconds=180)

        self.call_end_data = {
            "id": 17,
            "type": "end",
            "timestamp": end.isoformat(),
            "call_id": 2234,
         }

    def test_instantiate_call_end(self):
        event = CallEndEvent(**self.call_end_data)
        self.assertIsInstance(event, CallEndEvent)

    def test_process(self):
        event = CallEndEvent(**self.call_end_data)
        event.model = mock.Mock()
        event.process()
        event.model.handle_end.assert_called_once_with(event)
