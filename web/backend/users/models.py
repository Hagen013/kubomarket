from django.db import models
from django.contrib.auth.models import User


class UserProfile():

    class Meta:
        abstract = True 

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="нативный юзер"
    )

    name = models.CharField(
        verbose_name="имя"
    )

    surname = models.CharField(
        verbose_name="фамилия"
    )

    patronymic = models.CharField(
        verbose_name="отчество"
    )

    birth_date models.DateField(
        null=True,
        blank=True,
        verbose_name="дата рождения"
    )