from rest_framework.views import APIView
from rest_framework.response import Response
from api.serializers import GetCallBillSerializer
from apps.core.use_cases import GetCallBillUseCase


class CallBillView(APIView):
    serializer_class = GetCallBillSerializer
    use_case_class = GetCallBillUseCase

    def get(self, request, **kwargs):
        serializer = self.get_serializer(request.GET)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        use_case = self.get_use_case()
        data = use_case.execute(**serializer.data)
        return Response(data)

    def get_use_case(self):
        return self.use_case_class()

    def get_serializer(self, data):
        return self.serializer_class(data=data)
