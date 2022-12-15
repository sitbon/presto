# Presto! Requests

An object-oriented REST API client & requests extesion library.

As of version 1.0.0, this library can be considered stable, and significant
changes to the interface or new features are unlikely to be introduced.

#### Note: This library requires Python 3.11.0rc1 or later.

## Installation

```bash
pip install presto-requests
```
```bash
poetry add presto-requests
```

#### With async support using httpx:
```bash
pip install presto-requests[async]
```
```bash
poetry add presto-requests --extras async
```

### Concept:

Presto! Requests is a library that extends the functionality of the requests library.
It provides a simple way to create a REST API client that is object-oriented and easy to use.

### Example:

```python
from presto import Presto
import pprint

presto = Presto("https://api.github.com")

user = presto.users.sitbon()()  # == presto.users["sitbon"]().attr

print(f"User {user.login} has {user.public_repos} public repositories.")

pprint.pprint(dict(user))
```
```shell
User sitbon has 15 public repositories.
{'avatar_url': 'https://avatars.githubusercontent.com/u/1381063?v=4',
 'bio': None,
 'blog': '',
 'company': None,
 'created_at': '2012-01-26T04:25:21Z',
 'email': None,
 'events_url': 'https://api.github.com/users/sitbon/events{/privacy}',
 'followers': 7,
 'followers_url': 'https://api.github.com/users/sitbon/followers',
 'following': 13,
 'following_url': 'https://api.github.com/users/sitbon/following{/other_user}',
 'gists_url': 'https://api.github.com/users/sitbon/gists{/gist_id}',
 'gravatar_id': '',
 'hireable': None,
 'html_url': 'https://github.com/sitbon',
 'id': 1381063,
 'location': 'Portland, OR, USA',
 'login': 'sitbon',
 'name': 'Phillip Sitbon',
 'node_id': 'MDQ6VXNlcjEzODEwNjM=',
 'organizations_url': 'https://api.github.com/users/sitbon/orgs',
 'public_gists': 4,
 'public_repos': 15,
 'received_events_url': 'https://api.github.com/users/sitbon/received_events',
 'repos_url': 'https://api.github.com/users/sitbon/repos',
 'site_admin': False,
 'starred_url': 'https://api.github.com/users/sitbon/starred{/owner}{/repo}',
 'subscriptions_url': 'https://api.github.com/users/sitbon/subscriptions',
 'twitter_username': None,
 'type': 'User',
 'updated_at': '2022-11-22T00:41:18Z',
 'url': 'https://api.github.com/users/sitbon'}

```

### Usage:

Adding to a request path is as simple as accessing an attribute of the same name
from a `Presto` instance. For example, `Presto("http://example.com").some_path`
maps to a request object that defines a GET request to `http://example.com/some_path`.

Parameters such as headers are set by calling dotted objects under `Presto`, e.g. `presto.some_path(x=y)`.

These parameters are eventually passed to requests.request() as keyword arguments, but only
at a later time when the request is executed by calling the object without any arguments.

The return value from a parameter-setting call is the object itself, to enable further chaining.
Thus, request parameters can be set and inherited by further dotted paths.

Indexing the object like a list is a convient way to extend the path to a new object for things
like id paths, e.g. `Presto("http://<base>").note[1]` maps to a request for `http://<base>/note/1`
and calling that object executes the request.

There are a few special top-level attributes that can be used to modify the request without
needing to call the object and set the `method=` parameter:
`GET`, `POST`, `PUT`, `PATCH`, `DELETE`, `HEAD`, `OPTIONS`, and finally `R` which is
a request object with no path and no parameters set.


#### Example:

```python
from presto import Presto


presto = Presto(url="http://127.0.0.1:8000", APPEND_SLASH=True)

print("presto:", presto)

api = presto.api

print("api:", api)

note = api(headers={"X-User": "Testing"}).note

print("api.note:", api.note, "equal:", api.note == note)

resp = api.note[4]()

print("headers:", resp.request.headers)
print("response:", resp)
print("note:", resp.attr)
```
```shell
presto: Presto(url='http://127.0.0.1:8000/', params=adict(method='GET', headers={'Accept': 'application/json'}))
api: Request(url='http://127.0.0.1:8000/api/', params=adict(method='GET', headers={'Accept': 'application/json'}))
api.note: Request(url='http://127.0.0.1:8000/api/note/', params=adict(method='GET', headers={'Accept': 'application/json', 'X-User': 'Testing'})) equal: True
headers: {'User-Agent': 'python-requests/2.28.1', 'Accept-Encoding': 'gzip, deflate', 'Accept': 'application/json', 'Connection': 'keep-alive', 'X-User': 'Testing'}
response: <Response [200]>
note: adict(user='', id=4, url='http://127.0.0.1:8000/api/note/4/', time='2022-12-02T19:26:09-0800', note='Hello from the API!!', collection={'id': 3, 'url': 'http://127.0.0.1:8000/api/note/coll/3/', 'name': 'Public', 'public': True, 'notes': 1})
```

`response.attr` is an `adict` instance, which is a dictionary that can be accessed as attributes.
It contains the JSON-decoded content of a response, if any.

`APPEND_SLASH` is meant to be client implementation-specific, e.g. for a Django Rest Framework client, one would
typically set `Presto.APPEND_SLASH = True` or inherit from `Presto` in a pre-defined API client class.

# Async Support

Version 1.0.0 adds support for async requests using the `httpx` library.

The usage is the same as the synchronous version except when it comes to executing requests, so
calls to request objects without parameters need to be awaited. See the example below.

```python
import asyncio
from presto.asynco import AsyncPresto as Presto


async def main():
    presto = Presto(url="http://127.0.0.1:8000", APPEND_SLASH=True)

    print("presto:", presto)

    api = presto.api

    print("api:", api)

    note = api(headers={"X-User": "Testing"}).note

    print("api.note:", api.note, "equal:", api.note == note)

    resp = await api.note[4]()

    print("headers:", resp.request.headers)
    print("response:", resp)
    print("note:", resp.attr)

if __name__ == "__main__":
    asyncio.run(main())
```
```shell
presto: AsyncPresto(url='http://127.0.0.1:8000/', params=adict(method='GET', headers={'Accept': 'application/json'}))
api: Request(url='http://127.0.0.1:8000/api/', params=adict(method='GET', headers={'Accept': 'application/json'}))
api.note: Request(url='http://127.0.0.1:8000/api/note/', params=adict(method='GET', headers={'Accept': 'application/json', 'X-User': 'Testing'})) equal: True
headers: Headers({'host': '127.0.0.1:8000', 'accept-encoding': 'gzip, deflate', 'connection': 'keep-alive', 'user-agent': 'python-httpx/0.23.1', 'accept': 'application/json', 'x-user': 'Testing'})
response: <Response [200 OK]>
note: adict(user='', id=4, url='http://127.0.0.1:8000/api/note/4/', time='2022-12-02T19:26:09-0800', note='Hello from the API!!', collection={'id': 3, 'url': 'http://127.0.0.1:8000/api/note/coll/3/', 'name': 'Public', 'public': True, 'notes': 1})
```