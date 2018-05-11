from random import randint

from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.contrib.auth import login, logout, authenticate
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from core.utils import MailSender


class LoginView(TemplateView):
    template_name = "pages/login.html"

    def get(self, request, *args, **kwargs):
        is_authenticated = request.user.is_authenticated()
        if is_authenticated:
            return redirect("/")
        return super(LoginView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        is_authenticated = request.user.is_authenticated()
        if is_authenticated:
            return redirect("/")

        username, password = request.POST.get('email'), request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect("/")
        else:
            self.result = "error"
        return super(LoginView, self).get(request, *args, **kwargs)


class LogoutView(TemplateView):
    template_name = "pages/registration.html"

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("/")


class RegistrationView(TemplateView):
    template_name = "pages/registration.html"
    result = None

    def get(self, request, *args, **kwargs):
        is_authenticated = request.user.is_authenticated()
        if is_authenticated:
            return redirect("/")
        else:
            return super(RegistrationView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        is_authenticated = request.user.is_authenticated()
        if is_authenticated:
            return redirect("/")

        username, password = request.POST.get('email'), request.POST.get('password')

        try:
            validate_password(password)
        except ValidationError:
            self.result = "password_or_email_not_valid"
            return self.get(request, *args, **kwargs)

        if all((not is_authenticated, username, password)):
            user = User.objects.filter(username=username)
            if not user:
                user = User()
                user.username = username
                user.email = username
                user.set_password(password)

                j = "".join((str(randint(0, 9)) for _ in range(28)))

                user.first_name = j

                user.is_active = False
                try:
                    user.full_clean()
                except ValidationError:
                    self.result = "password_or_email_not_valid"
                    return self.get(request, *args, **kwargs)
                user.save()
                MailSender(
                    "Подтверждение почты",
                    "mail_templates/cod_dlya_uzera.html",
                    username,
                    context={
                        "user_id": user.id,
                        "cod": j
                    }
                ).send_mail()
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                self.result = "user_registered"
            else:
                self.result = "user_already_exists"
        else:
            self.result = "incorrect_data"
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(RegistrationView, self).get_context_data(**kwargs)
        context['result'] = self.result
        context['fromOauth'] = self.request.GET.get('from') == "oauth"
        # print(self.result)
        return context


class ProfileView(TemplateView):
    template_name = "pages/profile.html"

    def get(self, request, *args, **kwargs):
        is_authenticated = request.user.is_authenticated()
        if not is_authenticated:
            return redirect("/")
        return super(ProfileView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class ValidaciyaUzera(TemplateView):

    template_name = "pages/vu.html"

    def get(self, request, user_id, cod, **kwargs):
        user = get_object_or_404(User, pk=user_id)

        if user:
            if cod:
                if cod == user.first_name:
                    user.is_active = True
                    user.save()

        return redirect("/")
