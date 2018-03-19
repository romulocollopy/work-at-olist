from apps.core.models import Call as CallModel


class GetCallBillUseCase:

    def __init__(self, **kwargs):
        self.model = kwargs.get('model') or CallModel

    def execute(self, source=None, month=None, year=None, **kwargs):
        data = self.model.objects.month_bill(source, month=month, year=year)
        return data
