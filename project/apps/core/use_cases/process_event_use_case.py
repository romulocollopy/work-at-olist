from apps.core.models import StoredCallEvent
from apps.core.events import EventProcessor
from apps.core.factories import EventFactory


class ProcessEventUseCase:

    def __init__(self, **kwargs):
        self.model = kwargs.get('model') or StoredCallEvent
        self.processor = kwargs.get('processor') or EventProcessor()
        self.factory = kwargs.get('events_factory') or EventFactory()

    def execute(self, **kwargs):
        self.model.objects.create(**kwargs)
        event = self.factory.build(**kwargs)
        self.processor.process(event)
