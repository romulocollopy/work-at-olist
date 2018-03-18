from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from apps.core.services import PricingService


def _get_period(month, year):
    now = timezone.now()
    if month:
        year = year or now.year
    elif year:
        month = month or now.month
    else:
        month = 12 if now.month == 1 else now.month - 1
        year = year or (now.year - 1 if now.month == 1 else now.year)
    return int(month), int(year)


class CallQuerySet(models.QuerySet):

    def month_bill(self, source, month=None, year=None):
        month, year = _get_period(month, year)
        qs = self.filter(source=source) \
                 .filter(end_timestamp__month=month) \
                 .filter(end_timestamp__year=year) \
                 .filter(start_timestamp__isnull=False)
        return qs


class Call(models.Model):
    pricing_service = PricingService()
    objects = CallQuerySet.as_manager()

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
        call.clean()
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
        call.clean()
        call.save()

    def clean(self):
        super().clean()

        if self.duration and self.duration.total_seconds() < 0:
            raise ValidationError(
                {'duration': _("Call's duration cannot be negative.")}
            )

        if not (self.start_timestamp and self.end_timestamp):
            return

        if self.end_timestamp < self.start_timestamp:
            raise ValidationError(
                {'duration': _("Start time cannot be after end time")}
            )
