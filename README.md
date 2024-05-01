# Voltorb ⚡

![PyPI - Version](https://img.shields.io/pypi/v/voltorb?color=blue)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/voltorb?color=blue)
![PyPI - Status](https://img.shields.io/pypi/status/voltorb?color=lightgray)
![GitHub License](https://img.shields.io/github/license/amv213/voltorb?color=lightgray)
[![Nox](https://img.shields.io/badge/%F0%9F%A6%8A-Nox-D85E00.svg)](https://github.com/wntrblm/nox)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/charliermarsh/ruff)
[![Checked with mypy](https://img.shields.io/badge/mypy-checked-blue)](http://mypy-lang.org/)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)

A simple (unofficial) [Electricity Maps API](https://static.electricitymaps.com/api/docs/index.html) client

---

# Overview

**voltorb** is a simple (unofficial) client to the [Electricity Maps API](https://static.electricitymaps.com/api/docs/index.html).

Built on top of [**snug**](https://github.com/ariebovenberg/snug/tree/main), it provides a pythonic interface to query
and manipulate results from all of its available API endpoints and may generally be useful for explorative data analysis
and other applications.

> [!NOTE]
>
> This package is mainly a personal playground project to play around with a couple of libraries and
> concepts I am less familiar with (`snug`, `atts`, `cattrs`), and to refresh myself on the latest best-practices in
> terms of python tooling and packaging ecosystem.
>
> As such, please be careful if actually using this in production - the package API is still in very early development
> status!

# Installation

You can install `voltorb` from the python package index:

```shell
pip install voltorb
```

# Authentication

An API token is required to query most Electricity Maps API endpoints. If you do not already have one,
head over to https://api-portal.electricitymaps.com/ to explore all available options.

Once you have a token, you can setup token authentication as your authentication method:

```python
import voltorb

auth = voltorb.token_auth("MY-API-TOKEN")
```

Use this later as an authentication method when executing your API queries.


> [!TIP]
> To avoid hard-coding secrets, the following recipe uses `python-dotenv` to load the token from a local `.env` file:
>

```python
import os

import voltorb
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.environ.get("API_TOKEN")
auth = voltorb.token_auth(API_TOKEN)
```


# Quickstart

You can find queries for all [Electricity Maps API routes](https://static.electricitymaps.com/api/docs/index.html#routes) under the `voltorb.electricity_maps` namespace:

```python
import voltorb

zone = voltorb.ZoneKey("IT")
live_carbon_intensity = voltorb.electricity_maps.carbon_intensity.get_latest(zone)
```

and execute them against the API backend:

```python
import voltorb

response = voltorb.execute(live_carbon_intensity, auth=auth)
```

```shell
CarbonIntensity(
    zone='IT',
    carbon_intensity=327,
    datetime=datetime.datetime(2024, 4, 28, 21, 0, tzinfo=datetime.timezone.utc),
    updated_at=datetime.datetime(2024, 4, 28, 21, 47, 8, 110000, tzinfo=datetime.timezone.utc),
    created_at=datetime.datetime(2024, 4, 25, 21, 48, 58, 845000, tzinfo=datetime.timezone.utc),
    emission_factor_type=<EmissionFactorType.LIFECYCLE: 'lifecycle'>,
    is_estimated=True,
    estimation_method=<EstimationMethod.TIME_SLICER_AVERAGE: 'TIME_SLICER_AVERAGE'>
)
```

# Executing queries

Queries can be executed in different ways. We have already seen `execute()`, but `execute_async()` is also available
to perform asynchronous calls.

Both of these functions take arguments which affect:

- which authentication credentials are used
- which HTTP client is used (`voltorb` only includes basic sync and async HTTP clients)

For example, to use different credentials (or authentication methods):

```python
import voltorb

# use personal token for authentication
auth_personal = voltorb.token_auth("MY-PERSONAL-API_TOKEN")
voltorb.execute(query, auth=auth_personal)

# use commercial token for authentication
auth_commercial = voltorb.token_auth("MY-COMMERCIAL-API_TOKEN")
voltorb.execute(query, auth=auth_commercial)

# use no authentication (auth=None)
voltorb.execute(query)
```

And to use different backend HTTP clients (for example `httpx`):

```python
import httpx
import voltorb

with httpx.Client() as client:
    response = voltorb.execute(query, auth=auth, client=client)
```

You can also perform asynchronous queries through the same mechanisms:

```python
import aiohttp
import asyncio
import voltorb

async def main():

    response = await voltorb.execute_async(query, auth=auth)

    async with aiohttp.ClientSession() as client:
        response = await voltorb.execute_async(query, auth=auth, client=client)

asyncio.run(main())
```

> [!TIP]
> To make it easier to call `execute()`/`execute_async()` repeatedly with specific arguments, the
> `executor()`/`async_executor()` shortcuts can be used.

For example, to always add authentication to all of your queries:

```python
import voltorb

executor = voltorb.executor(auth=auth)

some_response = executor(some_query)
another_response = executor(another_query)

# we can still override arguments at execution time
unauthenticated_response = executor(yet_another_query, auth=None)
```
