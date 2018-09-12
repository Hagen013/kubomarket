from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser

from core.utils import MailSender


class EmailAPIView(APIView):

    permission_classes = (IsAdminUser,)

    def post(self, request, *args, **kwargs):
        email = request.data['email']
        text = request.data['text']
        mail_sender = MailSender(
            title="Подтверждение регистрации на сайте kubomarket.ru",
            template="mail_templates/user_verification.html",
            recipient=user_email,
            context=context
        )
        mail_sender.send()
        return Response({
        })