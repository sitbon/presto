# Presto! Requests

An object-oriented REST API client & requests extesion library.

Example:

```python
from pprint import pprint
from presto import Presto

presto = Presto('https://api.github.com')

user = presto.users.sitbon()  # == presto.users["sitbon"]()

print(f"User {user.attr.login} has {user.attr.public_repos} public repositories.")

pprint(user.json())
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