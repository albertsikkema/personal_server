TITLE: Define and Validate Data Models with Pydantic
DESCRIPTION: This example demonstrates how to define a data model using Pydantic's BaseModel. It showcases the use of Python type hints, default values, optional fields, and how Pydantic automatically validates and coerces external data into the defined model structure.
SOURCE: https://github.com/pydantic/pydantic/blob/main/README.md#_snippet_0

LANGUAGE: python
CODE:
```
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str = 'John Doe'
    signup_ts: Optional[datetime] = None
    friends: list[int] = []

external_data = {'id': '123', 'signup_ts': '2017-06-01 12:22', 'friends': [1, '2', b'3']}
user = User(**external_data)
print(user)
#> User id=123 name='John Doe' signup_ts=datetime.datetime(2017, 6, 1, 12, 22) friends=[1, 2, 3]
print(user.id)
#> 123
```

----------------------------------------

TITLE: Pydantic Model Validation Successful
DESCRIPTION: This snippet demonstrates how to define a Pydantic `BaseModel` and validate external data against it, showing successful data coercion and field access. It illustrates how Pydantic handles type annotations, default values, optional fields, and complex types like dictionaries with specific value constraints, along with automatic type coercion for various input formats.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/index.md#_snippet_1

LANGUAGE: python
CODE:
```
from datetime import datetime

from pydantic import BaseModel, PositiveInt


class User(BaseModel):
    id: int
    name: str = 'John Doe'
    signup_ts: datetime | None
    tastes: dict[str, PositiveInt]


external_data = {
    'id': 123,
    'signup_ts': '2019-06-01 12:22',
    'tastes': {
        'wine': 9,
        b'cheese': 7,
        'cabbage': '1',
    },
}

user = User(**external_data)

print(user.id)
# > 123
print(user.model_dump())
"""
{
    'id': 123,
    'name': 'John Doe',
    'signup_ts': datetime.datetime(2019, 6, 1, 12, 22),
    'tastes': {'wine': 9, 'cheese': 7, 'cabbage': 1},
}
"""
```

----------------------------------------

TITLE: Pydantic Model to Dictionary Conversion with `model.model_dump()`
DESCRIPTION: This section describes `model.model_dump()`, the primary method for converting a Pydantic model to a dictionary. It explains that sub-models are recursively converted and discusses parameters like `mode='json'` for JSON serializability, and options to include or exclude fields, including nested ones. It also notes exceptions for `RootModel` and the inclusion of computed fields.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/serialization.md#_snippet_0

LANGUAGE: Python
CODE:
```
from typing import Any, Optional

from pydantic import BaseModel, Field, Json


class BarModel(BaseModel):
    whatever: int


class FooBarModel(BaseModel):
    banana: Optional[float] = 1.1
    foo: str = Field(serialization_alias='foo_alias')
    bar: BarModel


m = FooBarModel(banana=3.14, foo='hello', bar={'whatever': 123})

# returns a dictionary:
print(m.model_dump())
#> {'banana': 3.14, 'foo': 'hello', 'bar': {'whatever': 123}}
print(m.model_dump(include={'foo', 'bar'}))
#> {'foo': 'hello', 'bar': {'whatever': 123}}
print(m.model_dump(exclude={'foo', 'bar'}))
#> {'banana': 3.14}
print(m.model_dump(by_alias=True))
#> {'banana': 3.14, 'foo_alias': 'hello', 'bar': {'whatever': 123}}
print(
    FooBarModel(foo='hello', bar={'whatever': 123}).model_dump(
        exclude_unset=True
    )
)
#> {'foo': 'hello', 'bar': {'whatever': 123}}
print(
    FooBarModel(banana=1.1, foo='hello', bar={'whatever': 123}).model_dump(
        exclude_defaults=True
    )
)
#> {'foo': 'hello', 'bar': {'whatever': 123}}
print(
    FooBarModel(foo='hello', bar={'whatever': 123}).model_dump(
        exclude_defaults=True
    )
)
#> {'foo': 'hello', 'bar': {'whatever': 123}}
print(
    FooBarModel(banana=None, foo='hello', bar={'whatever': 123}).model_dump(
        exclude_none=True
    )
)
#> {'foo': 'hello', 'bar': {'whatever': 123}}


class Model(BaseModel):
    x: list[Json[Any]]


print(Model(x=['{"a": 1}', '[1, 2]']).model_dump())
#> {'x': [{'a': 1}, [1, 2]]}
print(Model(x=['{"a": 1}', '[1, 2]']).model_dump(round_trip=True))
#> {'x': ['{"a":1}', '[1,2]']}
```

----------------------------------------

TITLE: Defining a Pydantic Model (Python)
DESCRIPTION: Defines a `User` model using Pydantic's `BaseModel`. It includes an required integer field `id` and an optional string field `name` with a default value. It also sets a configuration for string max length.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/models.md#_snippet_0

LANGUAGE: python
CODE:
```
from pydantic import BaseModel, ConfigDict


class User(BaseModel):
    id: int
    name: str = 'Jane Doe'

    model_config = ConfigDict(str_max_length=10)  # (1)!
```

----------------------------------------

TITLE: Install Pydantic Core Library
DESCRIPTION: Commands to install the Pydantic core library using pip, uv, and conda package managers. Pydantic requires Python 3.9+.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/install.md#_snippet_0

LANGUAGE: bash
CODE:
```
pip install pydantic
```

LANGUAGE: bash
CODE:
```
uv add pydantic
```

LANGUAGE: bash
CODE:
```
conda install pydantic -c conda-forge
```

----------------------------------------

TITLE: Install Pydantic V2
DESCRIPTION: Provides the command to install the latest production release of Pydantic V2 from PyPI. This is the recommended version for new projects and migrations.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/migration.md#_snippet_0

LANGUAGE: bash
CODE:
```
pip install -U pydantic
```

----------------------------------------

TITLE: Pydantic Model Validation and Serialization Example
DESCRIPTION: This Python example illustrates how Pydantic models perform validation and serialization. It uses `model_validate` to create an instance from input data and `model_dump` to serialize the model instance back into a dictionary, leveraging `pydantic-core` for high-performance operations.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/internals/architecture.md#_snippet_7

LANGUAGE: python
CODE:
```
from pydantic import BaseModel


class Model(BaseModel):
    foo: int


model = Model.model_validate({'foo': 1}) # (1)!
dumped = model.model_dump() # (2)!
```

----------------------------------------

TITLE: Defining Recursive JSON Type Alias with New Syntax (Python 3.12+)
DESCRIPTION: Defines a recursive `Json` type alias using the new `type` keyword syntax available in Python 3.12+. This syntax enables lazy evaluation, eliminating the need for forward annotation strings. The code validates the type using `pydantic.TypeAdapter` and outputs the corresponding JSON schema, showing the simplified definition compared to older Python versions.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/types.md#_snippet_11

LANGUAGE: Python
CODE:
```
from pydantic import TypeAdapter

type Json = dict[str, Json] | list[Json] | str | int | float | bool | None  # (1)!

ta = TypeAdapter(Json)
print(ta.json_schema())
"""
{
    '$defs': {
        'Json': {
            'anyOf': [
                {
                    'additionalProperties': {'$ref': '#/$defs/Json'},
                    'type': 'object',
                },
                {'items': {'$ref': '#/$defs/Json'}, 'type': 'array'},
                {'type': 'string'},
                {'type': 'integer'},
                {'type': 'number'},
                {'type': 'boolean'},
                {'type': 'null'}
            ]
        }
    },
    '$ref': '#/$defs/Json'
}
"""
```

----------------------------------------

TITLE: Defining Generic Pydantic Model (Python 3.12+ New Syntax)
DESCRIPTION: Illustrates the new PEP 695 syntax for defining generic Pydantic models in Python 3.12+, simplifying the declaration compared to older versions. Includes instantiation with different types and validation examples.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/models.md#_snippet_20

LANGUAGE: python
CODE:
```
from pydantic import BaseModel, ValidationError


class DataModel(BaseModel):
    number: int


class Response[DataT](BaseModel):  # (1)!
    data: DataT  # (2)!


print(Response[int](data=1))
#> data=1
print(Response[str](data='value'))
#> data='value'
print(Response[str](data='value').model_dump())
#> {'data': 'value'}

data = DataModel(number=1)
print(Response[DataModel](data=data).model_dump())
#> {'data': {'number': 1}}
try:
    Response[int](data='value')
except ValidationError as e:
    print(e)
    """
    1 validation error for Response[int]
    data
      Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='value', input_type=str]
    """
```

----------------------------------------

TITLE: Pydantic Model Serialization to Dict and JSON
DESCRIPTION: Demonstrates Pydantic's three serialization methods: to a Python dictionary of Python objects, to a dictionary of JSON-compatible types, and to a JSON string. It also shows how to customize output by excluding specific fields, unset values, or default values.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/why.md#_snippet_2

LANGUAGE: python
CODE:
```
from datetime import datetime

from pydantic import BaseModel


class Meeting(BaseModel):
    when: datetime
    where: bytes
    why: str = 'No idea'


m = Meeting(when='2020-01-01T12:00', where='home')
print(m.model_dump(exclude_unset=True))
#> {'when': datetime.datetime(2020, 1, 1, 12, 0), 'where': b'home'}
print(m.model_dump(exclude={'where'}, mode='json'))
#> {'when': '2020-01-01T12:00:00', 'why': 'No idea'}
print(m.model_dump_json(exclude_defaults=True))
#> {"when":"2020-01-01T12:00:00","where":"home"}
```

----------------------------------------

TITLE: Defining and Using Nested Pydantic Models - Python
DESCRIPTION: Shows how to create complex data structures by using Pydantic models as types within other models. Demonstrates instantiation with nested data and accessing the resulting model structure. Requires `pydantic.BaseModel` and `typing.Optional`.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/models.md#_snippet_9

LANGUAGE: python
CODE:
```
from typing import Optional

from pydantic import BaseModel


class Foo(BaseModel):
    count: int
    size: Optional[float] = None


class Bar(BaseModel):
    apple: str = 'x'
    banana: str = 'y'


class Spam(BaseModel):
    foo: Foo
    bars: list[Bar]


m = Spam(foo={'count': 4}, bars=[{'apple': 'x1'}, {'apple': 'x2'}])
print(m)
"""
foo=Foo(count=4, size=None) bars=[Bar(apple='x1', banana='y'), Bar(apple='x2', banana='y')]
"""
print(m.model_dump())
"""
{
    'foo': {'count': 4, 'size': None},
    'bars': [{'apple': 'x1', 'banana': 'y'}, {'apple': 'x2', 'banana': 'y'}],
}
"""
```

----------------------------------------

TITLE: Implementing Tagged Unions with Pydantic - Python
DESCRIPTION: This snippet demonstrates the implementation of a tagged (discriminated) union in Pydantic using `Literal` and `Field(discriminator='...')`. This pattern allows Pydantic to efficiently determine the correct model type within a union based on a specific field, significantly improving validation performance compared to untagged unions.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/performance.md#_snippet_5

LANGUAGE: python
CODE:
```
from typing import Any, Literal

from pydantic import BaseModel, Field


class DivModel(BaseModel):
    el_type: Literal['div'] = 'div'
    class_name: str | None = None
    children: list[Any] | None = None


class SpanModel(BaseModel):
    el_type: Literal['span'] = 'span'
    class_name: str | None = None
    contents: str | None = None


class ButtonModel(BaseModel):
    el_type: Literal['button'] = 'button'
    class_name: str | None = None
    contents: str | None = None


class InputModel(BaseModel):
    el_type: Literal['input'] = 'input'
    class_name: str | None = None
    value: str | None = None


class Html(BaseModel):
    contents: DivModel | SpanModel | ButtonModel | InputModel = Field(
        discriminator='el_type'
    )
```

----------------------------------------

TITLE: Demonstrating Pydantic Model Validation Methods (Python)
DESCRIPTION: This snippet defines a Pydantic `User` model and demonstrates the usage of `model_validate`, `model_validate_json`, and `model_validate_strings` for parsing and validating different input formats (dictionaries, JSON strings, string dictionaries). It also shows how `ValidationError` is raised for invalid inputs.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/models.md#_snippet_14

LANGUAGE: python
CODE:
```
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ValidationError


class User(BaseModel):
    id: int
    name: str = 'John Doe'
    signup_ts: Optional[datetime] = None


m = User.model_validate({'id': 123, 'name': 'James'})
print(m)
# id=123 name='James' signup_ts=None

try:
    User.model_validate(['not', 'a', 'dict'])
except ValidationError as e:
    print(e)
    # 1 validation error for User
    #   Input should be a valid dictionary or instance of User [type=model_type, input_value=['not', 'a', 'dict'], input_type=list]
    # 

m = User.model_validate_json('{"id": 123, "name": "James"}')
print(m)
# id=123 name='James' signup_ts=None

try:
    m = User.model_validate_json('{"id": 123, "name": 123}')
except ValidationError as e:
    print(e)
    # 1 validation error for User
    # name
    #   Input should be a valid string [type=string_type, input_value=123, input_type=int]
    # 

try:
    m = User.model_validate_json('invalid JSON')
except ValidationError as e:
    print(e)
    # 1 validation error for User
    #   Invalid JSON: expected value at line 1 column 1 [type=json_invalid, input_value='invalid JSON', input_type=str]
    # 

m = User.model_validate_strings({'id': '123', 'name': 'James'})
print(m)
# id=123 name='James' signup_ts=None

m = User.model_validate_strings(
    {'id': '123', 'name': 'James', 'signup_ts': '2024-04-01T12:00:00'}
)
print(m)
# id=123 name='James' signup_ts=datetime.datetime(2024, 4, 1, 12, 0)

try:
    m = User.model_validate_strings(
        {'id': '123', 'name': 'James', 'signup_ts': '2024-04-01'}, strict=True
    )
except ValidationError as e:
    print(e)
    # 1 validation error for User
    # signup_ts
    #   Input should be a valid datetime, invalid datetime separator, expected `T`, `t`, `_` or space [type=datetime_parsing, input_value='2024-04-01', input_type=str]
    # 
```

----------------------------------------

TITLE: Handling Pydantic Validation Errors in Python
DESCRIPTION: Demonstrates how Pydantic raises a `ValidationError` when an invalid value is assigned to a model field and the model is subsequently validated. It shows catching the exception and printing the error details.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/models.md#_snippet_17

LANGUAGE: python
CODE:
```
# note: setting `validate_assignment` to `True` in the config can prevent this kind of misbehavior.
m.a = 'not an int'

try:
    m2 = Model.model_validate(m)
except ValidationError as e:
    print(e)
```

----------------------------------------

TITLE: Pydantic TypeAdapter API Reference
DESCRIPTION: Reference for the `pydantic.type_adapter.TypeAdapter` class, which provides validation, serialization, and JSON schema generation capabilities for arbitrary Python types.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/type_adapter.md#_snippet_0

LANGUAGE: APIDOC
CODE:
```
pydantic.type_adapter.TypeAdapter
```

----------------------------------------

TITLE: Pydantic V1 to V2 Import Transformation
DESCRIPTION: Provides a general pattern for updating Pydantic V1 imports to be compatible with the `pydantic.v1` namespace in Pydantic V2. This is a key step for migrating existing V1 codebases.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/migration.md#_snippet_6

LANGUAGE: python
CODE:
```
from pydantic.<module> import <object>
```

LANGUAGE: python
CODE:
```
from pydantic.v1.<module> import <object>
```

----------------------------------------

TITLE: Pydantic V2 Field Optionality and Nullability Example
DESCRIPTION: Illustrates the new behavior of required, optional, and nullable fields in Pydantic V2, aligning more closely with `dataclasses`. It shows how `Optional[T]` fields are required by default if no default value is provided, and how different default values affect field optionality and nullability. Includes a `ValidationError` example.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/migration.md#_snippet_22

LANGUAGE: python
CODE:
```
from typing import Optional

from pydantic import BaseModel, ValidationError


class Foo(BaseModel):
    f1: str  # required, cannot be None
    f2: Optional[str]  # required, can be None - same as str | None
    f3: Optional[str] = None  # not required, can be None
    f4: str = 'Foobar'  # not required, but cannot be None


try:
    Foo(f1=None, f2=None, f4='b')
except ValidationError as e:
    print(e)
    """
    1 validation error for Foo
    f1
      Input should be a valid string [type=string_type, input_value=None, input_type=NoneType]
    """
```

----------------------------------------

TITLE: Pydantic Model Definition with Type Hints
DESCRIPTION: This example demonstrates how to define a Pydantic `BaseModel` using standard Python type hints for schema validation. It shows basic types like `str`, `Literal` for enumerated values, `Annotated` with `Gt` for constraints, and complex nested types like `dict` with `list` and `tuple`.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/why.md#_snippet_0

LANGUAGE: python
CODE:
```
from typing import Annotated, Literal

from annotated_types import Gt

from pydantic import BaseModel


class Fruit(BaseModel):
    name: str  # (1)!
    color: Literal['red', 'green']  # (2)!
    weight: Annotated[float, Gt(0)]  # (3)!
    bazam: dict[str, list[tuple[int, bool, float]]]  # (4)!


print(
    Fruit(
        name='Apple',
        color='red',
        weight=4.2,
        bazam={'foobar': [(1, True, 0.1)]},
    )
)
#> name='Apple' color='red' weight=4.2 bazam={'foobar': [(1, True, 0.1)]}
```

----------------------------------------

TITLE: Pydantic Field Validator: Accessing Validated Data with ValidationInfo.data
DESCRIPTION: Demonstrates how to use a Pydantic `field_validator` with `mode='after'` to compare two fields, such as `password` and `password_repeat`. It utilizes the `info.data` property of the `ValidationInfo` object to access the value of the `password` field that has already been validated.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/validators.md#_snippet_14

LANGUAGE: python
CODE:
```
from pydantic import BaseModel, ValidationInfo, field_validator


class UserModel(BaseModel):
    password: str
    password_repeat: str
    username: str

    @field_validator('password_repeat', mode='after')
    @classmethod
    def check_passwords_match(cls, value: str, info: ValidationInfo) -> str:
        if value != info.data['password']:
            raise ValueError('Passwords do not match')
        return value
```

----------------------------------------

TITLE: Pydantic Model to JSON String Conversion with `model.model_dump_json()`
DESCRIPTION: This section introduces `model.model_dump_json()`, a method that directly serializes a Pydantic model into a JSON-encoded string, producing results equivalent to `model.model_dump()`. It highlights Pydantic's ability to serialize types like `datetime` or `UUID` that `json.dumps` might not handle directly.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/serialization.md#_snippet_1

LANGUAGE: Python
CODE:
```
from datetime import datetime

from pydantic import BaseModel


class BarModel(BaseModel):
    whatever: int


class FooBarModel(BaseModel):
    foo: datetime
    bar: BarModel


m = FooBarModel(foo=datetime(2032, 6, 1, 12, 13, 14), bar={'whatever': 123})
print(m.model_dump_json())
#> {"foo":"2032-06-01T12:13:14","bar":{"whatever":123}}
print(m.model_dump_json(indent=2))
"""
{
  "foo": "2032-06-01T12:13:14",
  "bar": {
    "whatever": 123
  }
}
"""
```

----------------------------------------

TITLE: Pydantic Before Validator: Preprocess Input to Ensure List
DESCRIPTION: The `BeforeValidator` allows preprocessing of raw input values before Pydantic's standard validation. This example demonstrates how to use it to ensure a field's value is always a list, even if a single item is provided. It highlights the flexibility but also the responsibility to handle all possible input types. The example shows both the `Annotated` pattern and the `@field_validator` decorator approach.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/validators.md#_snippet_3

LANGUAGE: python
CODE:
```
from typing import Annotated, Any

from pydantic import BaseModel, BeforeValidator, ValidationError


def ensure_list(value: Any) -> Any:
    if not isinstance(value, list):
        return [value]
    else:
        return value


class Model(BaseModel):
    numbers: Annotated[list[int], BeforeValidator(ensure_list)]


print(Model(numbers=2))
try:
    Model(numbers='str')
except ValidationError as err:
    print(err)
```

LANGUAGE: python
CODE:
```
from typing import Any

from pydantic import BaseModel, ValidationError, field_validator


class Model(BaseModel):
    numbers: list[int]

    @field_validator('numbers', mode='before')
    @classmethod
    def ensure_list(cls, value: Any) -> Any:
        if not isinstance(value, list):
            return [value]
        else:
            return value


print(Model(numbers=2))
try:
    Model(numbers='str')
except ValidationError as err:
    print(err)
```

----------------------------------------

TITLE: Validating Single User Data with Pydantic and HTTPX (Python)
DESCRIPTION: This snippet demonstrates how to fetch a single user's data from an API using httpx and validate it against a Pydantic BaseModel. It defines a User model with id, name, and email fields, then uses User.model_validate() to parse the JSON response. The httpx.raise_for_status() method ensures that HTTP errors are caught.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/examples/requests.md#_snippet_0

LANGUAGE: Python
CODE:
```
import httpx

from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: int
    name: str
    email: EmailStr


url = 'https://jsonplaceholder.typicode.com/users/1'

response = httpx.get(url)
response.raise_for_status()

user = User.model_validate(response.json())
print(repr(user))
#> User(id=1, name='Leanne Graham', email='Sincere@april.biz')
```

----------------------------------------

TITLE: Custom Pydantic Datetime Validator for Timezone Constraint
DESCRIPTION: This Python code defines `MyDatetimeValidator` to enforce a specific timezone on a `datetime` object using Pydantic's `Annotated` type. It utilizes `__get_pydantic_core_schema__` with a `no_info_wrap_validator_function` to apply custom validation logic before and after Pydantic's default `datetime` validation. The validator raises an error if the `datetime`'s timezone does not match the specified constraint or if a naive datetime is provided when a constraint is set.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/examples/custom_validators.md#_snippet_0

LANGUAGE: python
CODE:
```
import datetime as dt
from dataclasses import dataclass
from pprint import pprint
from typing import Annotated, Any, Callable, Optional

import pytz
from pydantic_core import CoreSchema, core_schema

from pydantic import (
    GetCoreSchemaHandler,
    PydanticUserError,
    TypeAdapter,
    ValidationError,
)


@dataclass(frozen=True)
class MyDatetimeValidator:
    tz_constraint: Optional[str] = None

    def tz_constraint_validator(
        self,
        value: dt.datetime,
        handler: Callable,  # (1)!
    ):
        """Validate tz_constraint and tz_info."""
        # handle naive datetimes
        if self.tz_constraint is None:
            assert (
                value.tzinfo is None
            ), 'tz_constraint is None, but provided value is tz-aware.'
            return handler(value)

        # validate tz_constraint and tz-aware tzinfo
        if self.tz_constraint not in pytz.all_timezones:
            raise PydanticUserError(
                f'Invalid tz_constraint: {self.tz_constraint}',
                code='unevaluable-type-annotation',
            )
        result = handler(value)  # (2)!
        assert self.tz_constraint == str(
            result.tzinfo
        ), f'Invalid tzinfo: {str(result.tzinfo)}, expected: {self.tz_constraint}'

        return result

    def __get_pydantic_core_schema__(
        self,
        source_type: Any,
        handler: GetCoreSchemaHandler,
    ) -> CoreSchema:
        return core_schema.no_info_wrap_validator_function(
            self.tz_constraint_validator,
            handler(source_type),
        )


LA = 'America/Los_Angeles'
ta = TypeAdapter(Annotated[dt.datetime, MyDatetimeValidator(LA)])
print(
    ta.validate_python(dt.datetime(2023, 1, 1, 0, 0, tzinfo=pytz.timezone(LA)))
)
#> 2023-01-01 00:00:00-07:53

LONDON = 'Europe/London'
try:
    ta.validate_python(
        dt.datetime(2023, 1, 1, 0, 0, tzinfo=pytz.timezone(LONDON))
    )
except ValidationError as ve:
    pprint(ve.errors(), width=100)
    """
    [{'ctx': {'error': AssertionError('Invalid tzinfo: Europe/London, expected: America/Los_Angeles')},
    'input': datetime.datetime(2023, 1, 1, 0, 0, tzinfo=<DstTzInfo 'Europe/London' LMT-1 day, 23:59:00 STD>),
    'loc': (),
    'msg': 'Assertion failed, Invalid tzinfo: Europe/London, expected: America/Los_Angeles',
    'type': 'assertion_error',
    'url': 'https://errors.pydantic.dev/2.8/v/assertion_error'}]
    """
```

----------------------------------------

TITLE: Annotated with Optional Fields: Correct vs. Incorrect Metadata Placement
DESCRIPTION: Compares two ways of using `Annotated` with optional fields (`| None`), showing that `Field` metadata should be applied to the union type (`Annotated[int | None, ...]`) for it to affect the field, rather than just the base type (`Annotated[int, ...] | None`). This highlights the importance of applying metadata to the correct part of the type annotation.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/fields.md#_snippet_4

LANGUAGE: python
CODE:
```
class Model(BaseModel):
    field_bad: Annotated[int, Field(deprecated=True)] | None = None  # (1)!
    field_ok: Annotated[int | None, Field(deprecated=True)] = None  # (2)!
```

----------------------------------------

TITLE: Pydantic Datetime Field Handling with `datetime.datetime`
DESCRIPTION: This example illustrates how Pydantic processes `datetime.datetime` fields, accepting various formats such as ISO 8601 strings. It demonstrates the automatic parsing and conversion of a string representation into a `datetime` object, including timezone information, when assigned to a Pydantic model field.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/api/standard_library_types.md#_snippet_1

LANGUAGE: python
CODE:
```
from datetime import datetime

from pydantic import BaseModel


class Event(BaseModel):
    dt: datetime = None


event = Event(dt='2032-04-23T10:20:30.400+02:30')

print(event.model_dump())
```

----------------------------------------

TITLE: Pydantic After Model Validator Example
DESCRIPTION: Demonstrates an 'after' model validator in Pydantic, which runs post-initialization. This example checks if `password` and `password_repeat` fields match, raising a `ValueError` if they do not. The validated instance must be returned.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/validators.md#_snippet_10

LANGUAGE: python
CODE:
```
from typing_extensions import Self

from pydantic import BaseModel, model_validator


class UserModel(BaseModel):
    username: str
    password: str
    password_repeat: str

    @model_validator(mode='after')
    def check_passwords_match(self) -> Self:
        if self.password != self.password_repeat:
            raise ValueError('Passwords do not match')
        return self
```

----------------------------------------

TITLE: Basic RootModel Usage - Pydantic Python
DESCRIPTION: Demonstrates defining Pydantic models with a custom root type using `RootModel`, showing examples with a list of strings and a dictionary of strings. Includes validation, JSON dumping, and schema generation.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/models.md#_snippet_42

LANGUAGE: python
CODE:
```
from pydantic import RootModel

Pets = RootModel[list[str]]
PetsByName = RootModel[dict[str, str]]


print(Pets(['dog', 'cat']))
#> root=['dog', 'cat']
print(Pets(['dog', 'cat']).model_dump_json())
#> ["dog","cat"]
print(Pets.model_validate(['dog', 'cat']))
#> root=['dog', 'cat']
print(Pets.model_json_schema())
"""
{'items': {'type': 'string'}, 'title': 'RootModel[list[str]]', 'type': 'array'}
"""

print(PetsByName({'Otis': 'dog', 'Milo': 'cat'}))
#> root={'Otis': 'dog', 'Milo': 'cat'}
print(PetsByName({'Otis': 'dog', 'Milo': 'cat'}).model_dump_json())
#> {"Otis":"dog","Milo":"cat"}
print(PetsByName.model_validate({'Otis': 'dog', 'Milo': 'cat'}))
#> root={'Otis': 'dog', 'Milo': 'cat'}
```

----------------------------------------

TITLE: Optimizing TypeAdapter Instantiation (Good Example) - Python
DESCRIPTION: This snippet shows the recommended approach for using `TypeAdapter` by instantiating it once outside the function scope. This prevents redundant validator and serializer construction, improving performance by reusing the adapter across multiple function calls.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/performance.md#_snippet_1

LANGUAGE: python
CODE:
```
from pydantic import TypeAdapter

adapter = TypeAdapter(list[int])

def my_func():
    ...
    # do something with adapter
```

----------------------------------------

TITLE: Generate Top-Level JSON Schema with Multiple Pydantic Models
DESCRIPTION: Shows how to generate a top-level JSON schema that includes multiple Pydantic models and their related sub-models within the `$defs` section. This uses the `models_json_schema` function to combine schemas from different models into a single schema.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/json_schema.md#_snippet_28

LANGUAGE: python
CODE:
```
import json

from pydantic import BaseModel
from pydantic.json_schema import models_json_schema


class Foo(BaseModel):
    a: str = None


class Model(BaseModel):
    b: Foo


class Bar(BaseModel):
    c: int


_, top_level_schema = models_json_schema(
    [(Model, 'validation'), (Bar, 'validation')], title='My Schema'
)
print(json.dumps(top_level_schema, indent=2))
"""
{
  "$defs": {
    "Bar": {
      "properties": {
        "c": {
          "title": "C",
          "type": "integer"
        }
      },
      "required": [
        "c"
      ],
      "title": "Bar",
      "type": "object"
    },
    "Foo": {
      "properties": {
        "a": {
          "default": null,
          "title": "A",
          "type": "string"
        }
      },
      "title": "Foo",
      "type": "object"
    },
    "Model": {
      "properties": {
        "b": {
          "$ref": "#/$defs/Foo"
        }
      },
      "required": [
        "b"
      ],
      "title": "Model",
      "type": "object"
    }
  },
  "title": "My Schema"
}
"""
```

----------------------------------------

TITLE: Validating List of Users with Pydantic TypeAdapter and HTTPX (Python)
DESCRIPTION: This example illustrates how to validate a list of user objects retrieved from an API using Pydantic's TypeAdapter with httpx. It defines the same User BaseModel and then creates a TypeAdapter for list[User] to validate the entire JSON array response. This approach is useful for handling collections of models.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/examples/requests.md#_snippet_1

LANGUAGE: Python
CODE:
```
from pprint import pprint

import httpx

from pydantic import BaseModel, EmailStr, TypeAdapter


class User(BaseModel):
    id: int
    name: str
    email: EmailStr


url = 'https://jsonplaceholder.typicode.com/users/'  # (1)!

response = httpx.get(url)
response.raise_for_status()

users_list_adapter = TypeAdapter(list[User])

users = users_list_adapter.validate_python(response.json())
pprint([u.name for u in users])
"""
['Leanne Graham',
 'Ervin Howell',
 'Clementine Bauch',
 'Patricia Lebsack',
 'Chelsey Dietrich',
 'Mrs. Dennis Schulist',
 'Kurtis Weissnat',
 'Nicholas Runolfsdottir V',
 'Glenna Reichert',
 'Clementina DuBuque']
"""
```

----------------------------------------

TITLE: Serializing and Deserializing Data with Pydantic and Redis Queue (Python)
DESCRIPTION: This Python snippet demonstrates how to use Pydantic to serialize `User` model data into JSON before pushing it to a Redis queue and then deserialize and validate the data when popping it from the queue. It requires a running Redis server.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/examples/queues.md#_snippet_0

LANGUAGE: python
CODE:
```
import redis

from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: int
    name: str
    email: EmailStr


r = redis.Redis(host='localhost', port=6379, db=0)
QUEUE_NAME = 'user_queue'


def push_to_queue(user_data: User) -> None:
    serialized_data = user_data.model_dump_json()
    r.rpush(QUEUE_NAME, user_data.model_dump_json())
    print(f'Added to queue: {serialized_data}')


user1 = User(id=1, name='John Doe', email='john@example.com')
user2 = User(id=2, name='Jane Doe', email='jane@example.com')

push_to_queue(user1)
#> Added to queue: {"id":1,"name":"John Doe","email":"john@example.com"}

push_to_queue(user2)
#> Added to queue: {"id":2,"name":"Jane Doe","email":"jane@example.com"}


def pop_from_queue() -> None:
    data = r.lpop(QUEUE_NAME)

    if data:
        user = User.model_validate_json(data)
        print(f'Validated user: {repr(user)}')
    else:
        print('Queue is empty')


pop_from_queue()
#> Validated user: User(id=1, name='John Doe', email='john@example.com')

pop_from_queue()
#> Validated user: User(id=2, name='Jane Doe', email='jane@example.com')

pop_from_queue()
#> Queue is empty
```

----------------------------------------

TITLE: Custom Pydantic Datetime Validator for UTC Offset Bounds
DESCRIPTION: This Python example demonstrates a custom Pydantic validator that ensures a `datetime` object's UTC offset falls within a specified `lower_bound` and `upper_bound`. The `MyDatetimeValidator` class uses `__get_pydantic_core_schema__` to wrap the default Pydantic validation, asserting that the `datetime` has a UTC offset and that it is within the defined range (in hours). It raises an error if the offset is out of bounds or if the datetime is naive.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/examples/custom_validators.md#_snippet_1

LANGUAGE: python
CODE:
```
import datetime as dt
from dataclasses import dataclass
from pprint import pprint
from typing import Annotated, Any, Callable

import pytz
from pydantic_core import CoreSchema, core_schema

from pydantic import GetCoreSchemaHandler, TypeAdapter, ValidationError


@dataclass(frozen=True)
class MyDatetimeValidator:
    lower_bound: int
    upper_bound: int

    def validate_tz_bounds(self, value: dt.datetime, handler: Callable):
        """Validate and test bounds"""
        assert value.utcoffset() is not None, 'UTC offset must exist'
        assert self.lower_bound <= self.upper_bound, 'Invalid bounds'

        result = handler(value)

        hours_offset = value.utcoffset().total_seconds() / 3600
        assert (
            self.lower_bound <= hours_offset <= self.upper_bound
        ), 'Value out of bounds'

        return result

    def __get_pydantic_core_schema__(
        self,
        source_type: Any,
        handler: GetCoreSchemaHandler,
    ) -> CoreSchema:
        return core_schema.no_info_wrap_validator_function(
            self.validate_tz_bounds,
            handler(source_type),
        )


LA = 'America/Los_Angeles'  # UTC-7 or UTC-8
ta = TypeAdapter(Annotated[dt.datetime, MyDatetimeValidator(-10, -5)])
print(
```

----------------------------------------

TITLE: Handling Mutable Default Values in Pydantic Python
DESCRIPTION: Shows how Pydantic handles mutable default values (like lists or dictionaries). Unlike standard Python function arguments, Pydantic creates a deep copy of the mutable default value for each model instance if the value is not hashable, preventing unintended sharing of the default instance.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/fields.md#_snippet_9

LANGUAGE: python
CODE:
```
from pydantic import BaseModel


class Model(BaseModel):
    item_counts: list[dict[str, int]] = [{}]


m1 = Model()
m1.item_counts[0]['a'] = 1
print(m1.item_counts)

m2 = Model()
print(m2.item_counts)
```

----------------------------------------

TITLE: Pydantic V2: Changes to `Field` and JSON Schema Extra
DESCRIPTION: Pydantic V2's `Field` no longer supports arbitrary keyword arguments for JSON schema. Instead, `json_schema_extra` is used. The behavior of the `alias` property has changed, and several properties like `const`, `min_items`, `max_items`, `unique_items`, `allow_mutation`, `regex`, and `final` have been removed or replaced.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/migration.md#_snippet_13

LANGUAGE: APIDOC
CODE:
```
pydantic.Field:
  - `json_schema_extra`: Replaces arbitrary keyword arguments for adding data to JSON schema.
  - `alias` property: Returns `None` in V2 if no alias is set (V1 returned field name).
  - Removed/Changed properties:
    - `const` (removed)
    - `min_items` (use `min_length`)
    - `max_items` (use `max_length`)
    - `unique_items` (removed)
    - `allow_mutation` (use `frozen`)
    - `regex` (use `pattern`)
    - `final` (use `typing.Final` type hint)
  - Field constraints on generics:
    - No longer automatically pushed down to generic parameters.
    - Use `typing.Annotated` for inner type annotations.
      Example: `my_list: list[Annotated[str, Field(pattern=".*")]]`
```

----------------------------------------

TITLE: Define Alias for Validation and Serialization with Pydantic
DESCRIPTION: This snippet shows how to use `Field(alias='...')` in Pydantic to define an alias that is used for both model validation (instance creation) and serialization when `model_dump(by_alias=True)` is called. It requires `pydantic.BaseModel` and `pydantic.Field`.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/fields.md#_snippet_10

LANGUAGE: python
CODE:
```
from pydantic import BaseModel, Field


class User(BaseModel):
    name: str = Field(alias='username')


user = User(username='johndoe')  # (1)!
print(user)
#> name='johndoe'
print(user.model_dump(by_alias=True))  # (2)!
#> {'username': 'johndoe'}
```

----------------------------------------

TITLE: Using default_factory in Pydantic Python
DESCRIPTION: Shows how to use the `default_factory` argument of `pydantic.Field` to provide a callable that generates the default value when the model is instantiated. This is useful for creating dynamic or mutable default values.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/fields.md#_snippet_6

LANGUAGE: python
CODE:
```
from uuid import uuid4

from pydantic import BaseModel, Field


class User(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex)
```

----------------------------------------

TITLE: Customize Pydantic Field JSON Schema with `Field` Parameters
DESCRIPTION: This example demonstrates how to use `pydantic.fields.Field` parameters like `description`, `examples`, `title`, and `json_schema_extra` to customize the generated JSON Schema for a Pydantic model. It shows how to define a `User` model with various field types and their corresponding `Field` customizations, then prints the resulting JSON Schema.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/json_schema.md#_snippet_10

LANGUAGE: python
CODE:
```
import json

from pydantic import BaseModel, EmailStr, Field, SecretStr


class User(BaseModel):
    age: int = Field(description='Age of the user')
    email: EmailStr = Field(examples=['marcelo@mail.com'])
    name: str = Field(title='Username')
    password: SecretStr = Field(
        json_schema_extra={
            'title': 'Password',
            'description': 'Password of the user',
            'examples': ['123456'],
        }
    )


print(json.dumps(User.model_json_schema(), indent=2))
"""
{
  "properties": {
    "age": {
      "description": "Age of the user",
      "title": "Age",
      "type": "integer"
    },
    "email": {
      "examples": [
        "marcelo@mail.com"
      ],
      "format": "email",
      "title": "Email",
      "type": "string"
    },
    "name": {
      "title": "Username",
      "type": "string"
    },
    "password": {
      "description": "Password of the user",
      "examples": [
        "123456"
      ],
      "format": "password",
      "title": "Password",
      "type": "string",
      "writeOnly": true
    }
  },
  "required": [
    "age",
    "email",
    "name",
    "password"
  ],
  "title": "User",
  "type": "object"
}
"""
```

----------------------------------------

TITLE: Applying Numeric Constraints with Field - Python
DESCRIPTION: This example demonstrates how to apply various numeric constraints (`gt`, `ge`, `lt`, `le`, `multiple_of`, `allow_inf_nan`) to integer and float fields in a Pydantic model using `pydantic.Field`. It includes instantiation with values satisfying the constraints and printing the resulting model.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/fields.md#_snippet_18

LANGUAGE: python
CODE:
```
from pydantic import BaseModel, Field


class Foo(BaseModel):
    positive: int = Field(gt=0)
    non_negative: int = Field(ge=0)
    negative: int = Field(lt=0)
    non_positive: int = Field(le=0)
    even: int = Field(multiple_of=2)
    love_for_pydantic: float = Field(allow_inf_nan=True)


foo = Foo(
    positive=1,
    non_negative=0,
    negative=-1,
    non_positive=0,
    even=2,
    love_for_pydantic=float('inf'),
)
print(foo)
"""
positive=1 non_negative=0 negative=-1 non_positive=0 even=2 love_for_pydantic=inf
"""
```

----------------------------------------

TITLE: Defining Generic Pydantic Models and Subclasses (Python)
DESCRIPTION: Defines a generic base class `BaseClass` using `pydantic.BaseModel` and `typing.Generic` with type variables `TypeX` and `TypeY`. It then defines a generic subclass `ChildClass` that inherits from `BaseClass`, fixing `TypeX` to `int` and introducing a new type variable `TypeZ`.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/models.md#_snippet_23

LANGUAGE: python
CODE:
```
from typing import Generic, TypeVar

from pydantic import BaseModel

TypeX = TypeVar('TypeX')
TypeY = TypeVar('TypeY')
TypeZ = TypeVar('TypeZ')


class BaseClass(BaseModel, Generic[TypeX, TypeY]):
    x: TypeX
    y: TypeY


class ChildClass(BaseClass[int, TypeY], Generic[TypeY, TypeZ]):
    z: TypeZ
```

----------------------------------------

TITLE: Handling Pydantic Validation Errors (Python)
DESCRIPTION: Demonstrates Pydantic's error handling by defining a simple `BaseModel` with fields requiring specific types. Provides invalid input data and attempts to create a model instance within a `try...except ValidationError` block. Shows how the `ValidationError` captures multiple errors and provides detailed information about each failure.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/models.md#_snippet_13

LANGUAGE: python
CODE:
```
from pydantic import BaseModel, ValidationError


class Model(BaseModel):
    list_of_ints: list[int]
    a_float: float


data = dict(
    list_of_ints=['1', 2, 'bad'],
    a_float='not a float',
)

try:
    Model(**data)
except ValidationError as e:
    print(e)
    """
    2 validation errors for Model
    list_of_ints.2
      Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='bad', input_type=str]
    a_float
      Input should be a valid number, unable to parse string as a number [type=float_parsing, input_value='not a float', input_type=str]
    """
```

----------------------------------------

TITLE: Applying Constraints to Optional Fields with Annotated - Python
DESCRIPTION: This snippet demonstrates the recommended way to apply field constraints to optional fields in Pydantic using `typing.Annotated`. It shows how `Annotated` can wrap the type and the `Field` definition to avoid potential errors that might occur when applying constraints directly to `Optional` types.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/fields.md#_snippet_20

LANGUAGE: python
CODE:
```
from typing import Annotated, Optional

from pydantic import BaseModel, Field


class Foo(BaseModel):
    positive: Optional[Annotated[int, Field(gt=0)]]
    # Can error in some cases, not recommended:
    non_negative: Optional[int] = Field(ge=0)
```

----------------------------------------

TITLE: Defining Default Values in Pydantic Python
DESCRIPTION: Demonstrates the basic ways to provide default values for model fields using direct assignment or the `default` argument of `pydantic.Field`. Both methods make the field optional during model instantiation.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/fields.md#_snippet_5

LANGUAGE: python
CODE:
```
from pydantic import BaseModel, Field


class User(BaseModel):
    # Both fields aren't required:
    name: str = 'John Doe'
    age: int = Field(default=20)
```

----------------------------------------

TITLE: Defining a Pydantic Model Field with Field()
DESCRIPTION: Shows how to use `pydantic.fields.Field` to add metadata or constraints to a model field, like making it frozen. This form assigns the `Field` call to the field annotation.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/fields.md#_snippet_0

LANGUAGE: python
CODE:
```
from pydantic import BaseModel, Field


class Model(BaseModel):
    name: str = Field(frozen=True)
```