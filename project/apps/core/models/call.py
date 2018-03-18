from django.db import models
from apps.core.services import PricingService


class Call(models.Model):
    pricing_service = PricingService()

    source = models.CharField(max_length=11, null=True)
    destination = models.CharField(max_length=11, null=True)
    start_timestamp = models.DateTimeField(null=True)
    end_timestamp = models.DateTimeField(null=True)
    duration = models.DurationField(null=True)
    price = models.DecimalField(max_digits=11, decimal_places=2, null=True)

    @classmethod
    def handle_start(cls, event):
        call, created = cls.objects.update_or_create(
            id=event.call_id, defaults=dict(
                start_timestamp=event.timestamp,
                source=event.source,
                destination=event.destination,
            )
        )
        if created or call.end_timestamp is None:
            return
        call.duration = call.end_timestamp - event.timestamp
        call.price = cls.pricing_service.get_price(call)
        call.save()

    @classmethod
    def handle_end(cls, event):
        call, created = cls.objects.get_or_create(id=event.call_id)
        if created or call.start_timestamp is None:
            call.end_timestamp = event.timestamp
            call.save()
            return
        call.duration = event.timestamp - call.start_timestamp
        call.price = cls.pricing_service.get_price(call)
        call.save()
