import factory
from notes.models.models import Notes
from django.contrib.auth.models import User
from faker import Factory

faker = Factory.create()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model: User

    username = faker.name()
    password = "qwerty123"


class NotesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Notes
        django_get_or_create = ("title", "text")

    title = "Dummy Title"
    text = "Dummy Text"
    user = factory.SubFactory(UserFactory)
