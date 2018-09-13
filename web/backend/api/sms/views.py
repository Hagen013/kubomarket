from json.decoder import JSONDecodeError

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser

from core.utils import SMSMessage


class SMSAPIView(APIView):

    permission_classes = (IsAdminUser,)

    def post(self, request, *args, **kwargs):
        phone = request.data['phone']
        message = request.data['message']
        if phone is None or message is None:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )
        sms = SMSMessage(
            phone=phone,
            message=message,
        )
        response = sms.send()
        try:
            json = response.json()
        except JSONDecodeError:
            return Response(
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            json,
            status=status.HTTP_200_OK
        )


