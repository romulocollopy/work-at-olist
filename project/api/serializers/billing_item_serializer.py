import dateutil
from rest_framework import serializers


class BillingItemSerializer(serializers.Serializer):
    destination = serializers.CharField()
    start_date = serializers.SerializerMethodField()
    start_time = serializers.SerializerMethodField()
    duration = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    def get_start_date(self, obj):
        return obj.start_timestamp.date()

    def get_start_time(self, obj):
        return obj.start_timestamp.time()

    def get_duration(self, obj):
        delta = dateutil.relativedelta.relativedelta(
            seconds=obj.duration.total_seconds()
        )
        hours = delta.days * 24 + delta.hours
        minutes = int(delta.minutes)
        seconds = int(delta.seconds)
        return f"{hours}h{minutes}m{seconds}s"

    def get_price(self, obj):
        price = str(obj.price).replace('.', ',')
        return "R$ {}".format(price)
