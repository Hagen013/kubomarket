from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from users.models import Profile, UserComment
from users.serializers import ProfileSerializer, UserCommentSerializer
from cart.models import Order2
from cart.serializers import OrderSerializer


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


class UserContentAPIView(APIView):

    def check_user_permissions(self, request, pk):
        user_pk = getattr(request.user, "id", None)
        if user_pk != pk and not request.user.is_superuser:
            raise PermissionDenied

    def get(self, request, pk, *args, **kwargs):
        try:
            self.check_user_permissions(request, pk)
        except PermissionDenied:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return Response({
        })


class UserOrdersAPIView(UserContentAPIView):

    model = Order2
    serializer = OrderSerializer

    def get(self, request, pk, *args, **kwargs):
        super(UserOrdersAPIView, self).get(request, pk, *args, **kwargs)
        orders = self.model.objects.filter(user=request.user).order_by("-created_at")
        serializer = self.serializer(orders, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class UserProfileAPIView(UserContentAPIView):

    model = Profile
    serializer = ProfileSerializer

    def get(self, request, pk, *args,  **kwargs):
        super(UserProfileAPIView, self).get(request, pk, *args, **kwargs)
        serializer = self.serializer(request.user.profile)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class UserCommentsAPIView(UserContentAPIView):
    
    model = UserComment
    serializer = UserCommentSerializer

    def get(self, request, pk, *args, **kwargs):
        super(UserCommentsAPIView, self).get(request, pk, *args, **kwargs)
        return Response({})
