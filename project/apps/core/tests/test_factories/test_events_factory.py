from django.test import TestCase
from apps.core.factories import EventFactory


class EventFactoryTestCase(TestCase):

    def setUp(self):
        self.factory = EventFactory()

    def test_build(self):
        self.factory.build()
