from apps.core.models import Call as CallModel


class GetCallBillUseCase:

    def __init__(self, **kwargs):
        self.model = kwargs.get('model') or CallModel

    def execute(self, source=None, month=None, year=None, **kwargs):
        data = self.model.objects.month_bill(source, month=month, year=year)
        calls = [dict(
            destination=d.destination,
            start_date=d.start_timestamp.date(),
            start_time=d.start_timestamp.time(),
            duration=d.duration,
            price=d.price,
        ) for d in data]
        return dict(
            subscriber=source,
            period='{}/{}'.format(month, year),
            total=sum([d['price'] for d in calls]),
            calls=calls,
        )
