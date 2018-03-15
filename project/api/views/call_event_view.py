from rest_framework.views import APIView
from rest_framework.response import Response
from api.serializers import CallEventSerializer


class CallEventView(APIView):
    serializer_class = CallEventSerializer

    def post(self, request, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(status=400)

        return Response('OK')
