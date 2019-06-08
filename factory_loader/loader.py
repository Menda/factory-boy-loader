from typing import Any, List, Optional

from django.db import transaction

from . import utils


def _update_or_create(obj: Any, matching_fields: Optional[List[str]]) -> int:
    """
    Saves the factory in the database.
    """
    instance, pk, matching_fields = utils.build_obj(obj, matching_fields)

    kwargs = {}
    for field in matching_fields:
        kwargs[field] = getattr(instance, field)

    # Collect fields that do not have a ForeignKey or ManyToMany relation
    fields = []
    for field in instance._meta.get_fields():
        if not field.related_model:
            fields.append(field.name)

    for field in matching_fields:
        fields.remove(field)

    if pk in fields:
        fields.remove(pk)

    defaults = {}
    for field in fields:
        defaults[field] = getattr(instance, field)

    class_model = obj._meta.get_model_class()
    obj, _ = class_model.objects.update_or_create(**kwargs, defaults=defaults)
    return obj.id


@transaction.atomic
def load_factories(
        factories_module: str,
        matching_fields: Optional[List[str]] = None,
        truncate_table: bool = False) \
        -> None:
    if matching_fields is not None and type(matching_fields) is not list:
        raise ValueError('Invalid type for input parameter: matching_fields')
    elif matching_fields is not None and 'pk' in matching_fields:
        raise ValueError(
            '"pk" is not a valid field name for input parameter: '
            'matching_fields')

    visited = {}
    for obj in utils.get_classes(factories_module):
        id = _update_or_create(obj, matching_fields)
        if truncate_table:
            class_model = obj._meta.get_model_class()
            if class_model not in visited:
                visited[class_model] = []
            visited[class_model].append(id)

    for class_model in visited:
        class_model.objects.all().exclude(id__in=visited[class_model]).delete()
