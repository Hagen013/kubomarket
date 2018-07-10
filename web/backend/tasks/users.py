from django.contrib.auth.models import User

from config.celery import app
from users.tokens import account_activation_token
from core.utils import MailSender


@app.task
def user_verification(user_id):
    user = User.objects.get(id=user_id)
    user_email = user.username
    token = account_activation_token.make_token(user)
    user.first_name = token
    user.save()
    context = {
        "pk": user.id,
        "token": token
    }
    mail_sender = MailSender(
        title="Подтверждение регистрации на сайте kubomarket.ru",
        template="mail_templates/user_verification.html",
        recipient=user_email,
        context=context
    )
    mail_sender.send()


@app.task
def password_reset():
    pass
