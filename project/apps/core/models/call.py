from django.db import models


class Call(models.Model):
    pricing_service = None

    source = models.CharField(max_length=11)
    destination = models.CharField(max_length=11)
    start_timestamp = models.DateTimeField()
    duration = models.DurationField(null=True)
    price = models.DecimalField(max_digits=11, decimal_places=2, null=True)

    @classmethod
    def handle_start(cls, event):
        cls.objects.update_or_create(
            id=event.call_id, defaults=dict(
                start_timestamp=event.timestamp,
                source=event.source,
                destination=event.destination,
            )
        )

    @classmethod
    def handle_end(cls, event):
        call = cls.objects.get(id=event.call_id)
        call.duration = event.timestamp - call.start_timestamp
        call.price = cls.pricing_service.get_price(call)
        call.save()
