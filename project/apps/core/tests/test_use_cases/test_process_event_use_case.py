import mock
from datetime import datetime, timedelta
from django.test import TestCase
from apps.core.use_cases import ProcessEventUseCase


class ProcessEventUseCaseTestcase(TestCase):

    def setUp(self):
        self.model = mock.Mock()
        self.processor = mock.Mock()
        self.factory = mock.Mock()
        self.use_case = ProcessEventUseCase(
            model=self.model,
            processor=self.processor,
            events_factory=self.factory,
        )
        self.data = dict(span='eggs')

    def test_execute_saves_event(self):
        self.use_case.execute(**self.data)
        self.model.objects.update_or_create.assert_called_once_with(
            id=None, defaults=self.data)

    def test_execute_builds_event_with_factory(self):
        self.use_case.execute(**self.data)
        self.factory.build.assert_called_once_with(id=None, **self.data)

    def test_execute_procces_event(self):
        self.use_case.execute(**self.data)
        self.processor.process.assert_called_once_with(
            self.factory.build()
        )
