from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from notes.serializers.serializers import NotesSerializer, UserSerializer
from notes.models.models import Notes
from notes.tests.factories.Notes import NotesFactory

# Create your tests here.
class RegistrationTestCase(APITestCase):
    data = {
        "username": "unknown",
        "password": "pass7890",
        "password2": "pass7890",
        "email": "unknown@gmail.com",
        "first_name": "ABC",
        "last_name": "XYZ",
    }

    def test_registration(self):
        response = self.client.post("/register", RegistrationTestCase.data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_reg_same_username(self):
        response = self.client.post("/register", RegistrationTestCase.data)
        response2 = self.client.post("/register", RegistrationTestCase.data)
        self.assertEquals(response2.status_code, status.HTTP_400_BAD_REQUEST)


class UserDetailViewSetTestcase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="hamdan", password="qwerty123")

        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="JWT " + self.token.key)

    def test_user_authentication(self):
        response = self.client.get("/get-details")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login(self):
        data = {
            "username": "unknown",
            "password": "pass7890",
        }

        data1 = {
            "username": "unknown",
            "password": "pass7890",
            "password2": "pass7890",
            "email": "unknown@gmail.com",
            "first_name": "ABC",
            "last_name": "XYZ",
        }

        self.client.post("/register", data1)
        response = self.client.post("/login", data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)


class NotesViewsetTestCases(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="hamdan", password="qwerty123")
        self.client.force_authenticate(user=self.user)

    def test_add_note(self):
        data = {"title": "First Note", "text": "A dangerous not do not open"}

        response = self.client.post("/notes/", data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_delete_note(self):
        self.test_add_note()
        response = self.client.delete("/notes/1/")
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)


class notesModelsTestCase(APITestCase):
    # Todo: There is a conflict between keys
    def setUp(self):
        self.Note = NotesFactory()

    def test_Delete_Note(self):
        print(self.Note.id, self.Note)
        response = self.client.delete("/notes/1/")
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
