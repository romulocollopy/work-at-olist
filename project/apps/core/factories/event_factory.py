from apps.core.events.call_events import CallStartEvent, CallEndEvent


class EventFactory:

    def build(self, **kwargs):
        event_type = kwargs.get('type')
        if event_type == 'start':
            return CallStartEvent(**kwargs)
        if event_type == 'end':
            return CallEndEvent(**kwargs)
        raise ValueError(
            "{} is not a valid call event type".format(event_type)
        )
