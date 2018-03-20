from apps.core.models import Call as CallModel
from api.serializers import BillingItemSerializer


class GetCallBillUseCase:

    def __init__(self, **kwargs):
        self.model = kwargs.get('model') or CallModel

    def execute(self, source=None, month=None, year=None, **kwargs):
        qs = self.model.objects.month_bill(source, month=month, year=year)
        calls = BillingItemSerializer(qs, many=True)
        return dict(
            subscriber=source,
            period='{}/{}'.format(month, year),
            total=sum([c.price for c in qs]),
            calls=calls.data,
        )
