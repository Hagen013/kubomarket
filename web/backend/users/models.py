from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        blank=True,
        verbose_name="нативный юзер"
    )

    name = models.CharField(
        max_length=256,
        blank=True,
        verbose_name="имя"
    )

    surname = models.CharField(
        max_length=256,
        blank=True,
        verbose_name="фамилия"
    )

    patronymic = models.CharField(
        max_length=256,
        blank=True,
        verbose_name="отчество"
    )

    phone_number = models.CharField(
        max_length=64,
        blank=True,
        verbose_name="мобильный телефон"
    )

    birth_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="дата рождения"
    )

    @property
    def greeting_name(self):
        if self.name != "":
            return name
        else:
            return self.user.username


class UserComment(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        blank=True,
        verbose_name="юзер"
    )

    text = models.TextField(
        verbose_name="текст"
    )


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
