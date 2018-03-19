from datetime import datetime, timedelta
from django.test import TestCase
from api.serializers import CallEventSerializer


class CallEventSerializerTestCase(TestCase):

    def setUp(self):
        start = datetime(2018, 3, 3, 4, 3, 5)
        end = start + timedelta(seconds=180)
        self.call_start_data = {
            "id": 13,
            "type": "start",
            "timestamp": start.isoformat(),
            "call_id": 2234,
            "source":  "21999888777",
            "destination": "34777888999",
         }

        self.call_end_data = {
            "id": 17,
            "type": "end",
            "timestamp": end.isoformat(),
            "call_id": 2234,
         }

    def test_call_start_is_valid(self):
        serializer = CallEventSerializer(data=self.call_start_data)
        self.assertTrue(serializer.is_valid())

    def test_call_end_is_valid(self):
        serializer = CallEventSerializer(data=self.call_end_data)
        self.assertTrue(serializer.is_valid())

    def test_call_start_without_source(self):
        start_data = {
            k: v for k, v in self.call_start_data.items() if
            k != 'source'
        }
        serializer = CallEventSerializer(data=start_data)
        self.assertFalse(serializer.is_valid())

    def test_call_start_without_destination(self):
        start_data = {
            k: v for k, v in self.call_start_data.items() if
            k != 'destination'
        }
        serializer = CallEventSerializer(data=start_data)
        self.assertFalse(serializer.is_valid())

    def test_telephones_invalid_number(self):
        data = {k: v for k, v in self.call_start_data.items()}
        data['source'], data['destination'] = '123456789', '88888'
        serializer = CallEventSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('source', serializer.errors)
        self.assertIn('destination', serializer.errors)

    def test_telephones_invalid_type(self):
        data = {k: v for k, v in self.call_start_data.items()}
        data['source'], data['destination'] = 'AA34567890', 'XXAAABBBCCC'
        serializer = CallEventSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('source', serializer.errors)
        self.assertIn('destination', serializer.errors)
