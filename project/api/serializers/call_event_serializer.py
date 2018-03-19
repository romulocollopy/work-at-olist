from rest_framework import serializers
from apps.core.models.call import phone_validator


class CallEventSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=64)
    type = serializers.CharField(max_length=5)
    timestamp = serializers.DateTimeField()
    call_id = serializers.IntegerField()
    source = serializers.CharField(max_length=11, required=False)
    destination = serializers.CharField(max_length=11, required=False)

    def validate_source(self, value):
        phone_validator(value)
        return int(value)

    def validate_destination(self, value):
        phone_validator(value)
        return int(value)

    def validate(self, data):
        if data['type'] == 'start' and (
            not data.get('source') or
            not data.get('destination')
        ):
            raise serializers.ValidationError(
                "call start events must have source and destination numbers"
            )
        return data
