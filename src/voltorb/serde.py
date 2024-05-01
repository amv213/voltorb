"""Serialisation and deserialisation utilities."""

from collections.abc import Callable
from datetime import datetime
from typing import TypeVar

from attr import AttrsInstance
from attrs import fields
from cattrs import Converter
from cattrs.gen import (  # type: ignore[attr-defined]
    AttributeOverride,
    make_dict_structure_fn,
    override,
)


def to_whitespaced(snake_str: str) -> str:
    return snake_str.replace("_", " ")


def to_camel_case(snake_str: str) -> str:
    components = snake_str.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


K = TypeVar("K", bound=AttrsInstance)


def register_structure_hook(
    *,
    alias_generator: Callable[[str], str] | None = None,
    **kwargs: AttributeOverride,
) -> Callable[[type[K]], type[K]]:
    """A convenience class decorator to specify a custom specialized dict structuring function for an attrs class or
    dataclass.

    This is equivalent to converter.register_structure_hook(cls, make_dict_structure_fn(cls, converter, **kwargs)),
    but as a decorator, and with the shortcut of registering the hook on our single global converter.

    It also provides a special 'alias_generator' kwarg callable that can be used to conveniently generate aliases for
    all fields in a class on structuring (deserialisation). This is useful to use a consistent naming convention for
    all fields in a class, but don't want to specify the alias for each field individually.

    Note that this could be done as a one-liner using converter.register_unstructure_hook_factory but given that
    not all schemas use the same aliasing conventions this allows doing it on a per-schema basis and keep the logic
    close to the schema definition.

    References:
        https://catt.rs/en/stable/usage.html#using-factory-hooks
    """

    def decorator(cls: type[K]) -> type[K]:
        merged_kwargs = (
            {a.name: override(rename=alias_generator(a.name)) for a in fields(cls)}
            | kwargs
            if alias_generator is not None
            else kwargs
        )

        converter.register_structure_hook(
            cls,
            make_dict_structure_fn(
                cl=cls,
                converter=converter,
                **merged_kwargs,  # type: ignore[arg-type]
            ),
        )
        return cls

    return decorator


converter = Converter()

# specify how we want to structure datetime fields
converter.register_structure_hook(
    datetime,
    lambda isoformat, _: datetime.fromisoformat(isoformat.replace("Z", "+00:00")),
)
