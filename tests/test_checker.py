from django.test import TestCase
import pytest

from factory_loader import checker


class CheckFactoriesInterfaceTest(TestCase):
    def test_invalid_input_params(self):
        """
        Ensures that handles wrong params without breaking.
        """
        with pytest.raises(ValueError) as excinfo:
            checker.check_factories('tests.factories', {})
        assert str(excinfo.value) == \
            'Invalid type for input parameter: matching_fields'

        with pytest.raises(ValueError) as excinfo:
            checker.check_factories('tests.factories', ['pk'])
        assert str(excinfo.value) == \
            ('"pk" is not a valid field name for input parameter: '
             'matching_fields')

        with pytest.raises(ValueError) as excinfo:
            checker.check_factories('tests.factories', ['id', 'first_name'])
        assert str(excinfo.value) == \
            ('It is not possible to set a primary key together with another '
             'field')


class CheckFactoriesTest(TestCase):
    def test_simple(self):
        result, errors = checker.check_factories('tests.factories')
        assert result is True

        result, errors = checker.check_factories('tests.factories', ['id'])
        assert result is True

    def test_broken(self):
        result, errors = checker.check_factories('tests.factories_broken')
        assert result is False
        assert ('Error in factory: UserErikaFactory: It has no primary key '
                '"id" set') \
            in errors[0]

        result, errors = checker.check_factories('tests.factories_broken',
                                                 ['first_name', 'last_name'])
        assert result is False
        assert ('Error in factory: UserThatBreaksFactory: It is not possible '
                'to set a primary key "id" and use "matching_fields"') \
            in errors[0]

    def test_broken_ids(self):
        result, errors = checker.check_factories('tests.factories_broken_ids')
        assert result is False
        assert ('Error in factory "UserThatBreaksFactory". Has same matching '
                'field values "1" than') in errors[0]
