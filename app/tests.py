from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from .models import Character, Hat
from .serializers import CharacterSerializer, HatSerializer


class HatModelTestCase(TestCase):
    def setUp(self):
        self.hat = Hat.objects.create(color=Hat.Color.GREEN)
        self.client = APIClient()

    def test_create_hat(self):
        response = self.client.get(reverse('hat-detail', args=[self.hat.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_read_hat_list(self):
        response = self.client.get(reverse('hat-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_hat(self):
        # self.data = HatSerializer(self.hat).data
        self.new_data = {'color': 'P'}
        response = self.client.post(reverse('hat-list'), self.new_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_hat(self):
        self.data = HatSerializer(self.hat).data
        self.data.update({'color': Hat.Color.YELLOW})
        response = self.client.put(reverse('hat-detail', args=[self.hat.id]), self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_hat(self):
        response = self.client.delete(reverse('hat-detail', args=[self.hat.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class CharacterModelTestCase(TestCase):
    def setUp(self):
        self.hat = Hat.objects.create(color=Hat.Color.PURPLE)
        self.character = Character.objects.create(name="TestName", age=45, weight=50.0, human=True, hat=self.hat)
        self.client = APIClient()

    def test_create_character(self):
        response = self.client.get(reverse('hat-detail', args=[self.character.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_read_character_list(self):
        response = self.client.get(reverse('character-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_character(self):
        self.post_hat = Hat.objects.create(color=Hat.Color.PURPLE)
        self.data = {'name': "Test", 'age': 45, 'weight': 30.7, 'human': True, 'hat': self.post_hat.id}
        response = self.client.post(reverse('character-list'), self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_character(self):
        self.data = CharacterSerializer(self.character).data
        self.data.update({'name': 'TestName2', 'age': 13})
        response = self.client.put(reverse('character-detail', args=[self.character.id]), self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_character(self):
        response = self.client.delete(reverse('character-detail', args=[self.character.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # if character is deleted, associated hat is deleted
    def test_hat_one_to_one_strong_relationship(self):
        # check we can read hat
        response = self.client.get(reverse('hat-detail', args=[self.character.hat.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # delete character
        response = self.client.delete(reverse('character-detail', args=[self.character.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # check if associated hat has been deleted
        response = self.client.get(reverse('hat-detail', args=[self.character.hat.id]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_if_not_human_no_hat(self):
        self.hat_not_human = Hat.objects.create(color=Hat.Color.PURPLE)
        self.data = {'name': "TestName", 'age': 45, 'weight': 50.0, 'human': False, 'hat': self.hat_not_human.id}
        response = self.client.post(reverse('character-list'), self.data, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_if_p_in_name(self):
        self.yellow_hat = Hat.objects.create(color=Hat.Color.YELLOW)
        self.data = {'name': "Patrick", 'age': 45, 'weight': 30.7, 'human': True, 'hat': self.yellow_hat.id}
        response = self.client.post(reverse('character-list'), self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # if human weighs more than 80, must be more than 10 years old
    def test_weight_age(self):
        self.data = {'name': "Patrick", 'age': 8, 'weight': 85.2, 'human': True, 'hat': None}
        response = self.client.post(reverse('character-list'), self.data, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



