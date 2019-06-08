import factory

from .django_app import models


class UserJohnFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.User

    first_name = 'John'
    last_name = 'Doe'


class UserErikaFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.User

    first_name = 'Erika'
    last_name = 'Mustermann'


class UserThatBreaksFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.User

    id = 1
    first_name = 'Breaking'
    last_name = 'Bad'


class ToBeIgnored:
    pass
