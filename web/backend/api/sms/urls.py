from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser


class SMSAPIView(APIView):

    permission_classes = (IsAdminUser,)

    def post(self, request, *args, **kwargs):
        phone = request.data['phone']
        message = request.data['message']
        if phone is None or message is None:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )
        return Response({
        })

