from django.contrib.auth import authenticate, login
from django.shortcuts import redirect

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class SessionLoginAPIView(APIView):

    def get(self, request, *args, **kwargs):
        return Response({
            "user": request.user.is_superuser
        })

    def post(self, request, *args, **kwargs):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            return Response({}, status=status.HTTP_200_OK)

