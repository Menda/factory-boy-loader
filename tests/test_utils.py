from django.test import TestCase

from factory_loader import utils


class GetClassesTest(TestCase):
    def test_get_classes(self):
        obj_list = []
        for obj in utils.get_classes('tests.factories'):
            obj_list.append(obj.__name__)
        assert len(obj_list) == 2
        assert 'UserJohnFactory' in obj_list
        assert 'UserErikaFactory' in obj_list
