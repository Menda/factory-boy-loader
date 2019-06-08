# factory-boy-loader
 
factory-boy-loader is a tool that helps to load factories created
with factory_boy the same way that data fixtures are loaded in Django.

factory-boy was intended as an easy way to maintain fixtures for testing an
application, but does not provide a good way to populate an application with
initial datasets.

Use cases for this tool:

* An open demo application that needs to have cleaned and populated sample
  data nightly.
* An application that needs structural pre-populated data in order to work.
  E.g. it needs to have pre-defined users and groups stored in the
  database.
* An application that on every deployment, should create or update structural
  data.
* Share the same factories for both testing and production environment. This
  will allow the developer to become closer to the production environment when
  testing.


## Installation

```
pip install git+https://github.com/Menda/factory-boy-loader#egg=factory-boy-loader
```


## Usage

Let's suppose that we have the following structure:

```
myapp
├── factories
│   └── users.py
└── models.py
```

```
# factories/users.py

import factory
from .. import models

class UserJohnFactory(factory.Factory):
    class Meta:
        model = models.User

    pk = 1
    first_name = 'John'
    last_name = 'Doe'

class UserErikaFactory(factory.Factory):
    class Meta:
        model = models.User

    pk = 2
    first_name = 'Erika'
    last_name = 'Mustermann'
```

To load all factories:

```
from factory_loader import load_factories

load_factories('myapp.factories.users')
```

This will have had populated 2 users in database if users table was empty.

If the users table was not empty - let's suppose that we have a third user
with `pk=3` - it will update the current John and Erika users to the new
values (in case any of the factories changed), and the third user will stay
as is.

**Note:** even though it is not forbidden, it is not recommended to mix up
factories from different models in the same file.


## Reference


### `factory_loader.load_factories()`

`load_factories(factories_module: str, matching_fields: Optional[List[str]] = None, truncate_table: bool = False) -> None`

* `factories_module` is a string with the file where factories are defined.
* `matching_fields` list of strings with the fields used to fetch the object
from database to update it, or in case it is not found, create it. If it is
not set, it will default to PK. In some occasions this may become handy when
you do want to focus on content, but do not care about the PK.
* `truncate_table` is a boolean that indicates if all records need to be deleted
from the table or it should keep the old ones.


### `factory_loader.check_factories()`

`check_factories(factories_module: str, matching_fields: Optional[List[str]] = None) -> Tuple[bool, List[str]]`

* `factories_module` is a string with the file where factories are defined.
* `matching_fields` list of strings with the fields used to fetch the object
from database to update it, or in case it is not found, create it. If it is
not set, it will default to PK. In some occasions this may become handy when
you do want to focus on content, but do not care about the PK.

Returns a tuple a tuple `(success: bool, errors: list)` indicating if there is
any potential problem with the factories.

This function is ideal to be used in a test suite.


## Development

Firstly, install Docker.

Build the image:

```
docker-compose build
```

Enter into the container:

```
docker-compose run --rm --entrypoint 'sh' fbdl
```

Run the tests:

```
tox
```