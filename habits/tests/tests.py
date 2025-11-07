from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.utils import timezone
from unittest.mock import patch

from habits.models import UsefulHabit, PleasantHabit, Reword
from habits.serializers import UsefulHabitSerializer
from habits.tests.results import USEFUL_LIST_RESULT_1, USEFUL_LIST_RESULT_2, USEFUL_LIST_RESULT_3
from users.models import User


class AnUsefulHabitTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            username='test_user'
        )
        cls.user_2 = User.objects.create(
            username='test_user_2'
        )
        cls.reword = Reword.objects.create(
            name='test',
            description='test'
        )
        cls.pleasant_habit = PleasantHabit.objects.create(
            name='pleasant_test_name',
            owner=cls.user,
            location='test_loc',
            scheduled_time='2025-11-07T18:21:46.895014Z',
            action='test_action',
            periodicity=2,
            duration=30,
            is_public=True
        )
        cls.useful_habit_with_reword = UsefulHabit.objects.create(
            name='useful_with_reword',
            owner=cls.user,
            location='test_loc',
            scheduled_time='2025-11-07T18:21:46.895014Z',
            action='test_action',
            periodicity=2,
            duration=30,
            reword=cls.reword,
            is_public=True
        )
        cls.useful_habit_with_related = UsefulHabit.objects.create(
            name='useful_with_related',
            owner=cls.user,
            location='test_loc',
            scheduled_time='2025-11-07T18:21:46.895014Z',
            action='test_action',
            periodicity=2,
            duration=30,
            related_habit=cls.pleasant_habit,
            is_public=True
        )
        cls.useful_habit_with_reword_2 = UsefulHabit.objects.create(
            name='useful_with_reword_2',
            owner=cls.user_2,
            location='test_loc',
            scheduled_time='2025-11-07T18:21:46.895014Z',
            action='test_action',
            periodicity=2,
            duration=30,
            reword=cls.reword,
            is_public=True
        )

    def setUp(self):
        self.client.force_authenticate(user=self.user)

    def test_1_useful_list(self):
        # auth user
        url = reverse('habits:useful_my_list')
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        print(response.json())

        self.assertEqual(
            response.json(),
            USEFUL_LIST_RESULT_1
        )

        # auth user_2
        self.client.force_authenticate(user=self.user_2)
        response_2 = self.client.get(url)

        self.assertEqual(
            response_2.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response_2.json(),
            USEFUL_LIST_RESULT_2
        )

        # public
        url_2 = reverse('habits:useful_public_list')
        response_3 = self.client.get(url_2)

        self.assertEqual(
            response_3.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response_3.json(),
            USEFUL_LIST_RESULT_3
        )

    @patch("habits.tasks.send_simple_notification.delay")
    def test_2_useful_create(self, mock_task):
        url = reverse('habits:useful_create')
        data = {
            "name": "useful_with_reword_2",
            "owner": self.__class__.user.id,
            "location": "test_loc",
            "scheduled_time": "2025-11-07T18:21:46.895014Z",
            "action": "test_action",
            "periodicity": 2,
            "duration": 30,
            "reword": self.__class__.reword.id,
            "is_public": True
        }

        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        mock_task.assert_called_once()

        self.assertEqual(
            UsefulHabit.objects.all().count(),
            4
        )

        # reword + related_habit test
        data['related_habit'] = self.__class__.pleasant_habit.id

        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        mock_task.assert_called_once()

        self.assertEqual(
            UsefulHabit.objects.all().count(),
            4
        )

    def test_3_useful_retrieve(self):
        pk = self.__class__.useful_habit_with_reword.pk

        url = reverse('habits:useful_detail', args=(pk,))

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        habit = UsefulHabit.objects.get(pk=pk)
        self.assertEqual(
            response.json(),
            UsefulHabitSerializer(habit).data
        )

    @patch("habits.tasks.send_simple_notification.delay")
    def test_4_useful_update(self, mock_task):
        pk = self.__class__.useful_habit_with_reword.pk

        url = reverse('habits:useful_update', args=(pk,))

        put_response = self.client.put(
            url,
            data={
                "name": "useful_with_reword_2",
                "owner": self.__class__.user.id,
                "location": "test_loc",
                "scheduled_time": "2025-11-07T18:21:46.895014Z",
                "action": "test_action",
                "periodicity": 1,
                "duration": 30,
                "reword": self.__class__.reword.id,
                "is_public": True
            }
        )

        patch_response = self.client.patch(
            url,
            data={"duration": 50}
        )

        for resp in [put_response, patch_response]:
            self.assertEqual(
                resp.status_code,
                status.HTTP_200_OK
            )

        self.assertEqual(
            mock_task.call_count,
            2
        )

        habit = UsefulHabit.objects.get(pk=pk)

        self.assertEqual(
            UsefulHabitSerializer(habit).data['periodicity'],
            1
        )
        self.assertEqual(
            UsefulHabitSerializer(habit).data['duration'],
            50
        )

    @patch("habits.tasks.send_simple_notification.delay")
    def test_5_useful_delete(self, mock_task):
        pk = self.__class__.useful_habit_with_reword.pk
        url = reverse('habits:useful_delete', args=(pk,))

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        mock_task.assert_called_once()

        self.assertEqual(
            UsefulHabit.objects.all().count(),
            2
        )


class RewordTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.reword = Reword.objects.create(
            name='test',
            description='test'
        )
        cls.user = User.objects.create(
            username='test_user'
        )

    def setUp(self):
        self.client.force_authenticate(user=self.user)

    def test_6_reword_list(self):
        url = reverse('habits:reword-list')

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                'count': 1,
                'next': None,
                'previous': None,
                'results': [
                    {
                        'id': 2,
                        'name': 'test',
                        'description': 'test'
                    }
                ]
            }

        )
