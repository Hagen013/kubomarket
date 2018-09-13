from django.core.mail import EmailMessage

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser

from core.utils import MailSender


EMAIL_REPLY_TO = "info@kubomarket.ru"


class EmailAPIView(APIView):

    permission_classes = (IsAdminUser,)

    def post(self, request, *args, **kwargs):
        email = request.data['email']
        title = request.data['title']
        text = request.data['text']
        email = EmailMessage(
            title,
            text,
            to=[email],
            reply_to=[EMAIL_REPLY_TO],
        )
        email.send()
        return Response(
            status=status.HTTP_200_OK
        )
