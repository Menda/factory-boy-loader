import factory

from .django_app import models


class UserJohnFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.User

    first_name = 'John'
    last_name = 'Doe'


class BookJohnFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Book

    name = "John's book"
    author_id = 1
