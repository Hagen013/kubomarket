from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import redirect
from django.http import Http404
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist, ValidationError

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework.pagination import LimitOffsetPagination

from users.models import Profile, UserComment
from users.serializers import ProfileSerializer, UserCommentSerializer, UserSerializer
from cart.models import Order2
from cart.serializers import OrderSerializer
from tasks.users import user_verification


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


class SessionAuthAPIView(APIView):

    def post(self, request, *args, **kwargs):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user_exist = False
        stored_user = None
        try:
            stored_user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return Response(
                {"details": "username or password is invalid"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        if check_password(password, stored_user.password) and not stored_user.is_active:
            return Response(
                {"details": "user is not active"},
                status=status.HTTP_403_FORBIDDEN
            )
        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response(
                {"details": "not authenticated"},
                status=status.HTTP_401_UNAUTHORIZED
            )
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


class UserListAPIView(generics.ListCreateAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)
    pagination_class = LimitOffsetPagination

    def post(self, request, *args, **kwargs):
        is_authenticated = request.user.is_authenticated()
        if is_authenticated:
            return Response(
                {"detauls": "вы уже залогинены"},
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )

        username = request.POST.get("email")
        password = request.POST.get("password")

        try:
            validate_password(password)
        except ValidationError:
            return Response(
                {"details": "неправильный пароль"},
                status.HTTP_400_BAD_REQUEST
            )

        if all((not is_authenticated, username is not None, password is not None)):
            try:
                user = User.objects.get(username=username)
            except ObjectDoesNotExist:
                user = None
            if user is None:
                serializer = self.serializer_class(data=request.POST)
                if serializer.is_valid():
                    user = serializer.save()
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    user_verification.delay(user.id)
                    return Response(
                        {"details": "пользователь успешно зарегистрирован"},
                        status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        {"details": "email или пароль указаны неправильно"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    {"details": "пользователь с таким e-mail уже существует"},
                    status=status.HTTP_409_CONFLICT
                )


class UserApiView(UserContentAPIView):

    model = User
    serializer = UserSerializer

    def get_user(self, pk):
        try:
            instance = self.model.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise Http404
        return instance

    def get(self, request, pk, *args, **kwargs):
        super(UserApiView, self).get(request, pk, *args, **kwargs)
        user = self.get_user(pk=pk)
        serializer = self.serializer(user)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class UserOrdersAPIView(UserContentAPIView):

    model = Order2
    serializer = OrderSerializer

    def get(self, request, pk, *args, **kwargs):
        super(UserOrdersAPIView, self).get(request, pk, *args, **kwargs)
        orders = self.model.objects.filter(user=pk).order_by("-created_at")
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

    def put(self, request, pk, *args, **kwargs):
        super(UserProfileAPIView, self).get(request, pk, *args, **kwargs)
        pk = request.data.get("id", None)
        if pk is None:
            return Response(
                {"details": "id argument has not been provided"},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            instance = Profile.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(
                {"details": "profile with such id has not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.serializer(instance=instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"detauls": "invalid data provided"},
                status=status.HTTP_400_BAD_REQUEST
            )


class UserCommentsAPIView(UserContentAPIView):
    
    model = UserComment
    serializer = UserCommentSerializer

    def get(self, request, pk, *args, **kwargs):
        super(UserCommentsAPIView, self).get(request, pk, *args, **kwargs)
        return Response({})
