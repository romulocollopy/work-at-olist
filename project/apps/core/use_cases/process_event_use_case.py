from apps.core.models import StoredCallEvent
from apps.core.events import EventProcessor
from apps.core.factories import EventFactory


class ProcessEventUseCase:

    def __init__(self, **kwargs):
        self.model = kwargs.get('model') or StoredCallEvent
        self.processor = kwargs.get('processor') or EventProcessor()
        self.factory = kwargs.get('events_factory') or EventFactory()

    def execute(self, **kwargs):
        event_store_id = kwargs.pop('id') if 'id' in kwargs else None
        self.model.objects.update_or_create(id=event_store_id, defaults=kwargs)
        event = self.factory.build(**kwargs)
        self.processor.process(event)
