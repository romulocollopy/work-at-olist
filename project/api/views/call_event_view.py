from rest_framework.views import APIView
from rest_framework.response import Response
from api.serializers import CallEventSerializer
from apps.core.use_cases import ProcessEventUseCase


class CallEventView(APIView):
    serializer_class = CallEventSerializer
    use_case_class = ProcessEventUseCase

    def post(self, request, **kwargs):
        serializer = self.get_serializer(request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        use_case = self.get_use_case()
        use_case.execute(**serializer.data)
        return Response('OK')

    def get_use_case(self):
        return self.use_case_class()

    def get_serializer(self, data):
        return self.serializer_class(data=data)
