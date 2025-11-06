from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(verbose_name='Username', unique=True)
    email = models.EmailField(verbose_name="Email", unique=True, blank=True, null=True)
    telegram_chat_id = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Укажите chat_id от Telegram",
        help_text="Укажите chat_id от Telegram"
    )

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.username} - {self.email}"

    class Meta:
        verbose_name = "Пользователи"
        verbose_name_plural = "Пользователь"
