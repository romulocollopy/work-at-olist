from abc import ABC, abstractmethod

from apps.core.models import Call


class BaseEvent(ABC):
    model = Call

    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.timestamp = kwargs['timestamp']
        self.call_id = kwargs['call_id']

    @abstractmethod
    def process(self):
        pass


class CallStartEvent(BaseEvent):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source = kwargs['source']
        self.destination = kwargs['destination']

    def process(self):
        pass


class CallEndEvent(BaseEvent):

    def process(self):
        pass

