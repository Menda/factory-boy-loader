from typing import Any, List, Optional, Tuple

from . import utils
from .exceptions import ConflictError


def _process_obj(obj: Any, matching_fields: Optional[List[str]]) -> str:
    """
    :return: Key compound by the value of the matching fields.
    """
    instance, pk, matching_fields = utils.build_obj(obj, matching_fields)
    values = []
    for field in matching_fields:
        values.append(getattr(instance, field))
    return ', '.join(map(lambda v: str(v), values))


def check_factories(
        factories_module: str,
        matching_fields: Optional[List[str]] = None) \
        -> Tuple[bool, List[str]]:
    if matching_fields is not None and type(matching_fields) is not list:
        raise ValueError('Invalid type for input parameter: matching_fields')
    elif matching_fields is not None and 'pk' in matching_fields:
        raise ValueError(
            '"pk" is not a valid field name for input parameter: '
            'matching_fields')

    errors = []
    key_obj = {}
    for obj in utils.get_classes(factories_module):
        try:
            key = _process_obj(obj, matching_fields)
        except ConflictError as error:
            errors.append(str(error))
        else:
            if key in key_obj:
                errors.append(
                    f'Error in factory "{obj.__name__}". Has same matching '
                    f'field values "{key}" than "{key_obj[key]}"')
            else:
                key_obj[key] = obj

    success = False if errors else True
    return success, errors
