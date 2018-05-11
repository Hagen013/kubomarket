from rest_framework.views import APIView
from rest_framework.response import Response


class AuthenticationCheckAPIView(APIView):
    """
    Класс API проверки аутентификации пользователя
    """

    def get(self, request, *args, **kwargs):
        content = {
            'is_staff': request.user.is_staff
        }
        return Response(content)