from django.test import TestCase
import pytest

from factory_loader import loader, exceptions
from .django_app import models
from .factories import UserErikaFactory


class LoadFactoriesInterfaceTest(TestCase):
    def test_invalid_input_params(self):
        """
        Ensures that handles wrong params without breaking.
        """
        with pytest.raises(ValueError) as excinfo:
            loader.load_factories('tests.factories', {})
        assert str(excinfo.value) == \
            'Invalid type for input parameter: matching_fields'

        with pytest.raises(ValueError) as excinfo:
            loader.load_factories('tests.factories', ['pk'])
        assert str(excinfo.value) == \
            ('"pk" is not a valid field name for input parameter: '
             'matching_fields')

        with pytest.raises(ValueError) as excinfo:
            loader.load_factories('tests.factories', ['id', 'first_name'])
        assert str(excinfo.value) == \
            ('It is not possible to set a primary key together with another '
             'field')


class LoadFactoriesCreateTest(TestCase):
    def test_create_simple(self):
        """
        Ensures that the most simple happy path works.
        """
        loader.load_factories('tests.factories')
        assert models.User.objects.all().count() == 2
        user_john = models.User.objects.get(id=1)
        assert user_john.first_name == 'John'
        assert user_john.last_name == 'Doe'
        user_erika = models.User.objects.get(id=2)
        assert user_erika.first_name == 'Erika'
        assert user_erika.last_name == 'Mustermann'

    def test_create_simple_with_matching_fields(self):
        """
        Ensures that the most simple happy path works with matching_fields.
        """
        loader.load_factories('tests.factories', ['id'])
        assert models.User.objects.all().count() == 2

    def test_create_breaks(self):
        """
        Ensures that when something breaks, it does not make any change in
        database.
        """
        try:
            loader.load_factories('tests.factories_broken', ['first_name'])
        except exceptions.ConflictError:
            pass
        assert models.User.objects.all().count() == 0

    def test_create_truncate(self):
        class UserExtraUpdateFactory(UserErikaFactory):
            id = 3

        UserExtraUpdateFactory()

        loader.load_factories('tests.factories', truncate_table=True)
        assert models.User.objects.all().count() == 2

    def test_create_truncate_with_dependent_record(self):
        """
        Ensures that it does not fail truncating the table if there is a
        foreign key relationship to any user that is going to be updated.
        """
        class UserExtraUpdateFactory(UserErikaFactory):
            id = 3

        UserExtraUpdateFactory()
        loader.load_factories('tests.factories')

        user = models.User.objects.get(id=1)
        models.Book.objects.create(name='The Pythonist', author=user)

        loader.load_factories('tests.factories', truncate_table=True)
        assert models.User.objects.all().count() == 2


class LoadFactoriesUpdateTest(TestCase):
    def test_update(self):
        """
        Ensures that we update already created records.
        """
        loader.load_factories('tests.factories')

        class UserErikaUpdateFactory(UserErikaFactory):
            first_name = 'Erika Manuela'
            title = 'ms'

        loader._update_or_create(UserErikaUpdateFactory, ['id'])
        user_erika = models.User.objects.get(id=2)
        assert user_erika.first_name == 'Erika Manuela'
        assert user_erika.last_name == 'Mustermann'
        assert user_erika.title == 'ms'

    def test_update_compound_fetching_fields(self):
        """
        Ensures that we can update a record using two matching_fields and
        empty PK.
        """
        loader.load_factories('tests.factories')

        class UserErikaUpdateFactory(UserErikaFactory):
            id = None
            title = 'ms'

        loader._update_or_create(
            UserErikaUpdateFactory, ['first_name', 'last_name'])
        assert models.User.objects.all().count() == 2
        user_erika = models.User.objects.get(id=2)
        assert user_erika.first_name == 'Erika'
        assert user_erika.last_name == 'Mustermann'
        assert user_erika.title == 'ms'

    def test_update_compound_fetching_fields_but_pk_defined(self):
        """
        Ensures that we cannot update a record when we choose to use
        matching_fields but want also to pass a PK.
        """
        loader.load_factories('tests.factories')

        class UserErikaUpdateFactory(UserErikaFactory):
            id = 2

        with pytest.raises(exceptions.ConflictError) as excinfo:
            loader._update_or_create(
                UserErikaUpdateFactory, ['first_name', 'last_name'])
        assert str(excinfo.value) == \
            ('Error in factory: UserErikaUpdateFactory: It is not possible to '
             'set a primary key "id" and use "matching_fields"')
