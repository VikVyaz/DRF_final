from datetime import timedelta

from django.core.validators import MaxValueValidator
from django.db import models


class BaseHabit(models.Model):
    """Абстрактная модель для привычек"""

    PUBLIC_CHOICE = [
        (True, "Общий доступ"),
        (False, "Личное пользование")
    ]

    name = models.CharField(max_length=20, help_text='Название привычки')
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, help_text='Создатель привычки')
    location = models.CharField(help_text="Место, в котором необходимо выполнять привычку")
    scheduled_time = models.DateTimeField(help_text='Время, когда необходимо выполнять привычку')
    action = models.CharField(help_text='Действие, которое представляет собой привычка')
    periodicity = models.IntegerField(default=1, help_text='Периодичность выполнения привычки для напоминания(в днях)')
    duration = models.PositiveIntegerField(
        validators=[MaxValueValidator(120)],
        help_text='Время, которое потратит пользователь на выполнение привычки в секундах(максимум 120 сек)')
    is_public = models.BooleanField(choices=PUBLIC_CHOICE, help_text='Общий доступ для привычки')

    class Meta:
        abstract = True


class Reword(models.Model):
    """Модель вознаграждения для Полезной привычки"""

    name = models.CharField(help_text='Название вознаграждения')
    description = models.CharField(help_text='Описание вознаграждения')

    class Meta:
        verbose_name = "Вознаграждение"
        verbose_name_plural = "Вознаграждения"


class PleasantHabit(BaseHabit):
    """Модель приятной привычки"""

    is_pleasant = models.BooleanField(default=True, help_text='Индикатор приятной привычки (only True)')

    class Meta:
        verbose_name = "Приятная привычка"
        verbose_name_plural = "Приятные привычки"


class UsefulHabit(BaseHabit):
    """Модель полезной привычки"""

    is_pleasant = models.BooleanField(default=False, help_text='Индикатор полезной привычки (only False)')
    available = models.BooleanField(
        default=None,
        blank=True,
        null=True,
        help_text='Доступность привычки. '
                  '(True - привычка выполнялась меньше 7 дней назад, '
                  'False - привычка выполнялась больше 7 дней назад, '
                  'None/null - привычка еще не выполнялась)'
    )
    last_execution = models.DateTimeField(
        default=None,
        blank=True,
        null=True,
        help_text='Дата и время последнего выполнения привычки (None - не выполнялась)'
    )
    reword = models.ForeignKey(
        Reword,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Вознаграждение",
        help_text='Вознаграждение за выполнение привычки(взаимоисключающая со Связанной привычкой)'
    )
    related_habit = models.ForeignKey(
        PleasantHabit,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Связанная привычка",
        help_text='Связанная привычка (взаимоисключающая с Вознаграждением)'
    )

    class Meta:
        verbose_name = "Полезная привычка"
        verbose_name_plural = "Полезные привычки"
