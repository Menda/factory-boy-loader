from importlib import import_module
import inspect
from typing import Any, Iterator, List, Optional, Tuple

from .exceptions import ConflictError


def get_classes(factories_module: str) -> Iterator[str]:
    """
    Generator class that gets factory classes.
    """
    module = import_module(factories_module)
    for _, obj in inspect.getmembers(module):
        if type(obj).__module__.startswith('factory'):
            yield obj


def build_obj(obj: Any, matching_fields: Optional[List[str]]) \
        -> Tuple[Any, str, List[str]]:
    instance = obj.build()
    pk = instance._meta.pk.name

    if matching_fields is None:
        matching_fields = [pk]
    elif pk in matching_fields and len(matching_fields) > 1:
        raise ValueError(
            'It is not possible to set a primary key together with another '
            'field')

    if matching_fields != [pk] and getattr(instance, pk) is not None:
        raise ConflictError(
            f'Error in factory: {obj.__name__}: It is not possible to set a '
            f'primary key "{pk}" and use "matching_fields"')
    elif matching_fields == [pk] and getattr(instance, pk) is None:
        raise ConflictError(
            f'Error in factory: {obj.__name__}: It has no primary key "{pk}" '
            f'set')

    return instance, pk, matching_fields
