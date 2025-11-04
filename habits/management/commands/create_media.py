import os

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Создание media/ если отсутствует"

    def handle(self, *args, **options):
        media_path = settings.MEDIA_ROOT

        def create_dir(path, label):
            if not path:
                self.stdout.write(f"{label} в settings.py не указан")
                return

            try:
                os.makedirs(path, exist_ok=True)
                self.stdout.write(f"Папка {label} создана или уже существует")
            except Exception as e:
                self.stdout.write(f"Ошибка {e}")

        create_dir(media_path, "media")
