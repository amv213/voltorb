"""Patches for snug type annotations."""

import urllib.request
from collections.abc import Callable, Coroutine, Generator, Iterator
from typing import Any, Protocol, TypeAlias, TypeVar

import snug

T_co = TypeVar("T_co", covariant=True)
# this accounts for both simple generators and iterator-generators (as all generators are iterator[generator])
Query: TypeAlias = Iterator[Generator[snug.Request, snug.Response, T_co]]


_AuthT = Callable[[snug.Request], snug.Request] | tuple[str, str] | None


class Execute(Protocol):
    def __call__(
        self, query: Query[T_co], *, auth: _AuthT = ..., client: Any = ...
    ) -> T_co: ...


class ExecuteAsync(Protocol):
    def __call__(
        self, query: Query[T_co], *, auth: _AuthT = ..., client: Any = ...
    ) -> Coroutine[Any, Any, T_co]: ...


def execute(query: Query[T_co], auth: _AuthT = None, client: Any = None) -> T_co:
    if client is None:
        client = urllib.request.build_opener()
    return snug.execute(query, auth, client)  # type: ignore[no-any-return]


def execute_async(
    query: Query[T_co], auth: _AuthT = None, client: Any = None
) -> Coroutine[Any, Any, T_co]:
    return snug.execute_async(query, auth, client)  # type: ignore[no-any-return]


def executor(**kwargs: Any) -> Execute:
    return snug.executor(**kwargs)  # type: ignore[no-any-return]


def async_executor(**kwargs: Any) -> ExecuteAsync:
    return snug.async_executor(**kwargs)  # type: ignore[no-any-return]
