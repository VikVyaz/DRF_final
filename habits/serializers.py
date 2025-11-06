from rest_framework import serializers

from habits.models import PleasantHabit, UsefulHabit, Reword


class UsefulHabitSerializer(serializers.ModelSerializer):
    """Сериализатор UsefulHabit"""

    class Meta:
        model = UsefulHabit
        fields = "__all__"
        read_only_fields = ('is_pleasant',)

    def validate(self, attrs):
        """Валидация полей reword и related_habit"""

        reword_field = attrs.get('reword', False)
        related_habit_field = attrs.get('related_habit', False)

        if reword_field and related_habit_field:
            raise serializers.ValidationError(
                "Либо Вознаграждение, либо Связанная привычка"
            )

        if attrs.get('related_habit', False):
            if not attrs.related_habit.is_pleasant:
                raise serializers.ValidationError(
                    "Связанной привычкой может быть только Приятная привычка"
                )

        return attrs


class PleasantHabitSerializer(serializers.ModelSerializer):
    """Сериализатор PleasantHabit"""

    class Meta:
        model = PleasantHabit
        fields = "__all__"
        read_only_fields = ('is_pleasant',)


class RewordSerializer(serializers.ModelSerializer):
    """Сериализатор Reword"""

    class Meta:
        model = Reword
        fields = "__all__"
