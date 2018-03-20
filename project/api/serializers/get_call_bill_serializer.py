from django.utils import timezone
from rest_framework import serializers


class GetCallBillSerializer(serializers.Serializer):
    source = serializers.CharField()
    month = serializers.IntegerField(required=False)
    year = serializers.IntegerField(required=False)

    def validate(self, data):
        month, year = self._get_period(data.get('month'), data.get('year'))
        return dict(
            source=data['source'],
            month=month,
            year=year,
        )

    def _get_period(self, month, year):
        now = timezone.now()
        if month:
            year = year or now.year
        elif year:
            month = month or now.month
        else:
            month = 12 if now.month == 1 else now.month - 1
            year = year or (now.year - 1 if now.month == 1 else now.year)
        return int(month), int(year)
