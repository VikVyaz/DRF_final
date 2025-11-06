from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated

from habits.models import PleasantHabit, Reword, UsefulHabit
from habits.paginators import HabitPaginator, RewordPaginator
from habits.permissions import HabitPermission
from habits.serializers import PleasantHabitSerializer, UsefulHabitSerializer, RewordSerializer
from habits.tasks import send_simple_notification


class RewordViewSet(viewsets.ModelViewSet):
    queryset = Reword.objects.all()
    serializer_class = RewordSerializer
    pagination_class = RewordPaginator


class PleasantHabitViewSet(viewsets.ModelViewSet):
    queryset = PleasantHabit.objects.all()
    serializer_class = PleasantHabitSerializer
    pagination_class = HabitPaginator

    # permission_classes = [IsAuthenticated, HabitPermission]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class MyUsefulHabitListView(generics.ListAPIView):
    serializer_class = UsefulHabitSerializer
    pagination_class = HabitPaginator

    # permission_classes = [IsAuthenticated, HabitPermission]

    def get_queryset(self):
        user = self.request.user
        queryset = UsefulHabit.objects.all()

        return queryset.filter(owner=user)


class PublicUsefulHabitListView(generics.ListAPIView):
    serializer_class = UsefulHabitSerializer
    pagination_class = HabitPaginator
    permission_classes = [IsAuthenticated, HabitPermission]

    def get_queryset(self):
        queryset = UsefulHabit.objects.all()

        return queryset.filter(is_public=True)


class UsefulHabitCreateView(generics.CreateAPIView):
    queryset = UsefulHabit.objects.all()
    serializer_class = UsefulHabitSerializer
    pagination_class = HabitPaginator
    permission_classes = [IsAuthenticated, HabitPermission]

    def perform_create(self, serializer):
        habit = serializer.save(owner=self.request.user)
        send_simple_notification.delay(
            f'Привычка "{habit.name}" создана.',
            habit.owner.telegram_chat_id
        )


class UsefulHabitRetrieveView(generics.RetrieveAPIView):
    queryset = UsefulHabit.objects.all()
    serializer_class = UsefulHabitSerializer
    pagination_class = HabitPaginator
    permission_classes = [IsAuthenticated, HabitPermission]


class UsefulHabitUpdateView(generics.UpdateAPIView):
    queryset = UsefulHabit.objects.all()
    serializer_class = UsefulHabitSerializer
    pagination_class = HabitPaginator
    permission_classes = [IsAuthenticated, HabitPermission]

    def perform_update(self, serializer):
        habit = serializer.save()
        send_simple_notification.delay(
            f'Привычка "{habit.name}" изменена.',
            habit.owner.telegram_chat_id
        )


class UsefulHabitDestroyView(generics.DestroyAPIView):
    queryset = UsefulHabit.objects.all()
    serializer_class = UsefulHabitSerializer
    pagination_class = HabitPaginator
    permission_classes = [IsAuthenticated, HabitPermission]

    def perform_destroy(self, instance):
        send_simple_notification.delay(
            f'Привычка "{instance.name}" удалена.',
            instance.owner.telegram_chat_id
        )
        instance.delete()
