import mock
from django.test import TestCase
from apps.core.events import EventProcessor


class EventProcessorTestCase(TestCase):

    def setUp(self):
        self.event = mock.Mock()
        self.processor = EventProcessor()

    def test_process(self):
        self.processor.process(self.event)
        self.event.process.assert_called_once_with()
