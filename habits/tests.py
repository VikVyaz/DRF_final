from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import UsefulHabit, PleasantHabit, Reword


class UsefulHabitTestCase(APITestCase):

    def setUp(self):
        # self.reword = Reword.objects.create()
        pass
