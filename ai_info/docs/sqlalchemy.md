# sqlalchemy Documentation
> Source: https://context7.com/sqlalchemy/sqlalchemy/llms.txt
> Retrieved: 2025-06-27

TITLE: Iterating Results with Core Select via Session.execute().scalars()
DESCRIPTION: The SQLAlchemy 2.0 approach to iterating over results from a Core select() construct executed via Session.execute(), including joins and filters. The scalars() modifier is used to yield ORM objects.
SOURCE: https://github.com/sqlalchemy/sqlalchemy/blob/main/doc/build/changelog/migration_20.rst#_snippet_66

LANGUAGE: Python
CODE:
```
for user in session.execute(
    select(User).join(User.addresses).filter(Address.email == "some@email.case")
).scalars():
    ...
```

----------------------------------------

TITLE: Creating a SQLAlchemy Engine (Python)
DESCRIPTION: Demonstrates the basic usage of `sqlalchemy.create_engine` to establish a connection pool to a database using a connection URL. This engine instance is typically created once per application process and manages multiple DBAPI connections.
SOURCE: https://github.com/sqlalchemy/sqlalchemy/blob/main/doc/build/core/connections.rst#_snippet_0

LANGUAGE: python
CODE:
```
engine = create_engine("mysql+mysqldb://scott:tiger@localhost/test")
```

----------------------------------------

TITLE: Defining SQLAlchemy ORM Models and Table in Python
DESCRIPTION: This snippet defines the core SQLAlchemy ORM model classes (User, Address, Order, Item) using Declarative Mapping and a standard Table object for a many-to-many relationship. It establishes relationships between models and defines table names and columns with primary keys and foreign keys. These classes represent the database schema used for subsequent query examples.
SOURCE: https://github.com/sqlalchemy/sqlalchemy/blob/main/doc/build/orm/queryguide/_plain_setup.rst#_snippet_0

LANGUAGE: python
CODE:
```
from typing import List
from typing import Optional

from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import ForeignKey
from sqlalchemy import Table
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session


class Base(DeclarativeBase):
    pass
class User(Base):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    fullname: Mapped[Optional[str]]
    addresses: Mapped[List["Address"]] = relationship(back_populates="user")
    orders: Mapped[List["Order"]] = relationship()

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"
class Address(Base):
    __tablename__ = "address"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    email_address: Mapped[str]
    user: Mapped[User] = relationship(back_populates="addresses")

    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"
order_items_table = Table(
    "order_items",
    Base.metadata,
    Column("order_id", ForeignKey("user_order.id"), primary_key=True),
    Column("item_id", ForeignKey("item.id"), primary_key=True),
)

class Order(Base):
    __tablename__ = "user_order"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    items: Mapped[List["Item"]] = relationship(secondary=order_items_table)
class Item(Base):
    __tablename__ = "item"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str]
```

----------------------------------------

TITLE: Bulk Insert with RETURNING using session.scalars in SQLAlchemy ORM
DESCRIPTION: Demonstrates performing a bulk insert operation using the sqlalchemy.dml.Insert construct with the returning() clause. The operation is executed via session.scalars(), passing a list of dictionaries for the rows to be inserted. This method optimizes batching and supports heterogeneous parameter sets.
SOURCE: https://github.com/sqlalchemy/sqlalchemy/blob/main/doc/build/changelog/whatsnew_20.rst#_snippet_24

LANGUAGE: Python
CODE:
```
users = session.scalars(
    insert(User).returning(User),
    [
        {"name": "spongebob", "fullname": "Spongebob Squarepants"},
        {"name": "sandy", "fullname": "Sandy Cheeks"},
        {"name": "patrick", "fullname": "Patrick Star"},
        {"name": "squidward", "fullname": "Squidward Tentacles"},
        {"name": "ehkrabs", "fullname": "Eugene H. Krabs"},
    ],
)
print(users.all())
```

----------------------------------------

TITLE: Using Outermost Transaction Block (Preferred Pattern) - SQLAlchemy Python
DESCRIPTION: Presents the recommended SQLAlchemy 2.0 pattern for transaction management. The transaction is explicitly started using `with session.begin():` at the outermost scope where database operations occur. Inner functions like `method_a` and `method_b` do not need to manage transactions themselves, simplifying the code and making transaction boundaries clear.
SOURCE: https://github.com/sqlalchemy/sqlalchemy/blob/main/doc/build/changelog/migration_20.rst#_snippet_102

LANGUAGE: Python
CODE:
```
def method_a(session):
    method_b(session)

def method_b(session):
    session.add(SomeObject("bat", "lala"))


Session = sessionmaker(engine)

# create a Session and call method_a
with Session() as session:
    with session.begin():
        method_a(session)
```

----------------------------------------

TITLE: Defining ForeignKey ON UPDATE/ON DELETE in SQLAlchemy
DESCRIPTION: Demonstrates how to specify ON UPDATE and ON DELETE clauses for Foreign Key constraints using the `onupdate` and `ondelete` keyword arguments in `ForeignKey` (for single columns) and `ForeignKeyConstraint` (for composite keys). These options control cascading behavior upon parent row modifications.
SOURCE: https://github.com/sqlalchemy/sqlalchemy/blob/main/doc/build/core/constraints.rst#_snippet_8

LANGUAGE: Python
CODE:
```
child = Table(
    "child",
    metadata_obj,
    Column(
        "id",
        Integer,
        ForeignKey("parent.id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    ),
)

composite = Table(
    "composite",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("rev_id", Integer),
    Column("note_id", Integer),
    ForeignKeyConstraint(
        ["rev_id", "note_id"],
        ["revisions.id", "revisions.note_id"],
        onupdate="CASCADE",
        ondelete="SET NULL",
    ),
)
```

----------------------------------------

TITLE: Defining Scalar Default for INSERT - SQLAlchemy Python
DESCRIPTION: This snippet demonstrates how to set a simple scalar default value for a column using the `default` parameter of `Column`. The value '12' will be used during an INSERT statement if no value is provided for 'somecolumn'.
SOURCE: https://github.com/sqlalchemy/sqlalchemy/blob/main/doc/build/core/defaults.rst#_snippet_0

LANGUAGE: Python
CODE:
```
Table("mytable", metadata_obj, Column("somecolumn", Integer, default=12))
```

----------------------------------------

TITLE: Defining a Declarative Base Class in SQLAlchemy
DESCRIPTION: This snippet defines a foundational `Base` class by inheriting from `DeclarativeBase`. This `Base` class serves as the common ancestor for all ORM-mapped classes, providing the necessary infrastructure for declarative table and object mapping.
SOURCE: https://github.com/sqlalchemy/sqlalchemy/blob/main/doc/build/orm/declarative_tables.rst#_snippet_0

LANGUAGE: Python
CODE:
```
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
```

----------------------------------------

TITLE: Declaring User Mapped Class with Declarative (Python)
DESCRIPTION: Defines the `User` class, inheriting from the `Base` Declarative class, to represent the 'user_account' table. It uses `__tablename__` to name the table and `Mapped`/`mapped_column` for column definitions, including a primary key, string columns using `String(30)`, and a relationship to 'Address' objects. Requires standard SQLAlchemy imports for types like `String` and ORM constructs.
SOURCE: https://github.com/sqlalchemy/sqlalchemy/blob/main/doc/build/tutorial/metadata.rst#_snippet_10

LANGUAGE: python
CODE:
```
from typing import List
from typing import Optional
from sqlalchemy import String # Requires import from sqlalchemy
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]

    addresses: Mapped[List["Address"]] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"
```

----------------------------------------

TITLE: Executing a SELECT Statement and Processing Results
DESCRIPTION: Shows how to execute a previously constructed `Select` object (`stmt`) using `session.execute`. The resulting `Result` object is then processed using `scalars()` to yield ORM entity instances directly, which are then iterated over to print attribute values. Includes the generated SQL.
SOURCE: https://github.com/sqlalchemy/sqlalchemy/blob/main/doc/build/orm/queryguide/select.rst#_snippet_1

LANGUAGE: python
CODE:
```
result = session.execute(stmt)
for user_obj in result.scalars():
    print(f"{user_obj.name} {user_obj.fullname}")
```

LANGUAGE: sql
CODE:
```
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account
WHERE user_account.name = ?
```

----------------------------------------

TITLE: Defining Basic Many-to-One (Annotated Declarative) - Python
DESCRIPTION: This snippet demonstrates a simple, non-bidirectional Many-to-One relationship using annotated Declarative. The foreign key is on the parent table, referencing the child, and the scalar relationship attribute is declared on the parent class.
SOURCE: https://github.com/sqlalchemy/sqlalchemy/blob/main/doc/build/orm/basic_relationships.rst#_snippet_6

LANGUAGE: Python
CODE:
```
class Parent(Base):
    __tablename__ = "parent_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    child_id: Mapped[int] = mapped_column(ForeignKey("child_table.id"))
    child: Mapped["Child"] = relationship()


class Child(Base):
    __tablename__ = "child_table"

    id: Mapped[int] = mapped_column(primary_key=True)
```

----------------------------------------

TITLE: Defining Declarative Base Class (SQLAlchemy 2.0) - Python
DESCRIPTION: Demonstrates the new way to define the base class for declarative models in SQLAlchemy 2.0 using `DeclarativeBase`, which is better understood by typing tools compared to the function `declarative_base`. This is the first step in migrating existing mappings.
SOURCE: https://github.com/sqlalchemy/sqlalchemy/blob/main/doc/build/changelog/whatsnew_20.rst#_snippet_12

LANGUAGE: Python
CODE:
```
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass
```

----------------------------------------

TITLE: ORM Annotated Declarative Mapping with Type Annotations
DESCRIPTION: This example showcases the modern SQLAlchemy 2.0 approach using `Mapped` type annotations with `mapped_column()`. SQLAlchemy can infer column types and nullability from the annotations, allowing for more concise and type-safe model definitions while still enabling explicit `mapped_column` arguments for overrides.
SOURCE: https://github.com/sqlalchemy/sqlalchemy/blob/main/doc/build/orm/declarative_tables.rst#_snippet_3

LANGUAGE: Python
CODE:
```
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    fullname: Mapped[str | None]
    nickname: Mapped[str | None] = mapped_column(String(30))
```

----------------------------------------

TITLE: Defining SQLAlchemy ORM Mapped Class with DeclarativeBase
DESCRIPTION: This snippet defines a basic ORM mapped class `MyTable` using the modern DeclarativeBase. It maps to a table named "my_table" with an integer primary key `id` and a string column `name`. This class is used in subsequent examples demonstrating `schema_translate_map` and `identity_token`.
SOURCE: https://github.com/sqlalchemy/sqlalchemy/blob/main/doc/build/orm/queryguide/api.rst#_snippet_6

LANGUAGE: Python
CODE:
```
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass


class MyTable(Base):
    __tablename__ = "my_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
```

----------------------------------------

TITLE: Subqueryload with Limit Potential Issue - SQLAlchemy
DESCRIPTION: Demonstrates the problem when using `subqueryload` with `LIMIT` but no `ORDER BY`. The `LIMIT` is pushed into the subquery, potentially causing the main and load queries to operate on different sets of rows if the database doesn't provide a deterministic order.
SOURCE: https://github.com/sqlalchemy/sqlalchemy/blob/main/doc/build/faq/ormconfiguration.rst#_snippet_15

LANGUAGE: python
CODE:
```
>>> user = session.scalars(
...     select(User).options(subqueryload(User.addresses)).limit(1)
... ).first()
```

LANGUAGE: sql
CODE:
```
-- the "main" query
SELECT users.id AS users_id
FROM users
 LIMIT 1
```

LANGUAGE: sql
CODE:
```
-- the "load" query issued by subqueryload
SELECT addresses.id AS addresses_id,
       addresses.user_id AS addresses_user_id,
       anon_1.users_id AS anon_1_users_id
FROM (SELECT users.id AS users_id FROM users LIMIT 1) AS anon_1
JOIN addresses ON anon_1.users_id = addresses.user_id
ORDER BY anon_1.users_id
```

----------------------------------------

TITLE: Simplify SQLAlchemy ORM Mapping with Mapped (Typed and Concise) - Python
DESCRIPTION: This snippet demonstrates a further simplified version of the SQLAlchemy ORM declarative models, leveraging Python type annotations with `Mapped` to imply column types and nullability. It shows how `mapped_column` can be omitted or simplified when type annotations provide sufficient information.
SOURCE: https://github.com/sqlalchemy/sqlalchemy/blob/main/doc/build/changelog/whatsnew_20.rst#_snippet_16

LANGUAGE: Python
CODE:
```
from typing import List
from typing import Optional
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]
    addresses: Mapped[List["Address"]] = relationship(back_populates="user")


class Address(Base):
    __tablename__ = "address"

    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    user: Mapped["User"] = relationship(back_populates="addresses")
```

----------------------------------------

TITLE: Fetch with Joined Eager Loading (SQLAlchemy 2.0)
DESCRIPTION: Shows the 2.0 approach for fetching objects and eagerly loading a related collection using `select` with `options(joinedload(...))`, applying `.unique()` to handle potential duplicates from the join, and fetching all results using `.all()`. Requires a configured SQLAlchemy session, mapped User class, and the `select` and `joinedload` functions.
SOURCE: https://github.com/sqlalchemy/sqlalchemy/blob/main/doc/build/changelog/migration_20.rst#_snippet_46

LANGUAGE: Python
CODE:
```
session.scalars(
  select(User).
  options(
    joinedload(User.addresses)
  )
).unique().all()
```

----------------------------------------

TITLE: Using SQLAlchemy Session with Context Manager
DESCRIPTION: Demonstrates the basic pattern for creating a SQLAlchemy Engine and Session, adding objects, and committing changes using a Python context manager (`with` statement). This ensures the session is automatically closed.
SOURCE: https://github.com/sqlalchemy/sqlalchemy/blob/main/doc/build/orm/session_basics.rst#_snippet_0

LANGUAGE: Python
CODE:
```
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

# an Engine, which the Session will use for connection
# resources
engine = create_engine("postgresql+psycopg2://scott:tiger@localhost/")

# create session and add objects
with Session(engine) as session:
    session.add(some_object)
    session.add(some_other_object)
    session.commit()
```

----------------------------------------

TITLE: Building SELECT Statement with Method Chaining (Python)
DESCRIPTION: This snippet demonstrates how to construct a SQLAlchemy `select` statement using the 'generative' or method chaining pattern. It shows adding multiple criteria with `.where()` and an ordering clause with `.order_by()`, where each method call returns a new, modified select object.
SOURCE: https://github.com/sqlalchemy/sqlalchemy/blob/main/doc/build/glossary.rst#_snippet_7

LANGUAGE: Python
CODE:
```
stmt = (
    select(user.c.name)
    .where(user.c.id > 5)
    .where(user.c.name.like("e%"))
    .order_by(user.c.name)
)
```

----------------------------------------

TITLE: Defining One-to-Many Relationship with Delete Cascade in SQLAlchemy
DESCRIPTION: This Python snippet defines a `User` model with a one-to-many relationship to `Address` objects. The `cascade="all, delete"` option is specified, indicating that when a `User` object is deleted via the ORM session, related `Address` objects will also be deleted.
SOURCE: https://github.com/sqlalchemy/sqlalchemy/blob/main/doc/build/orm/cascades.rst#_snippet_10

LANGUAGE: python
CODE:
```
class User(Base):
  # ...

  addresses = relationship("Address", cascade="all, delete")
```

----------------------------------------

TITLE: Performing a Simple ORM Join using Relationship in SQLAlchemy
DESCRIPTION: Demonstrates how to use `select().join()` with a relationship attribute (`User.addresses`) to automatically construct a JOIN clause between the `User` and `Address` entities based on the defined relationship. The resulting SQL joins the `user_account` and `address` tables on the foreign key relationship.
SOURCE: https://github.com/sqlalchemy/sqlalchemy/blob/main/doc/build/orm/queryguide/select.rst#_snippet_19

LANGUAGE: Python
CODE:
```
stmt = select(User).join(User.addresses)
```

LANGUAGE: SQL
CODE:
```
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account JOIN address ON user_account.id = address.user_id
```

----------------------------------------

TITLE: Defining Select Statement with Row Typing in SQLAlchemy
DESCRIPTION: This Python snippet demonstrates how to define a simple SELECT statement using SQLAlchemy's SQL Expression Language. In SQLAlchemy 2.0, this statement would be typed as `Select[Tuple[int, str]]`, while in 2.1 it is typed more directly as `Select[int, str]` leveraging PEP 646 for improved type checking of row contents.
SOURCE: https://github.com/sqlalchemy/sqlalchemy/blob/main/doc/build/changelog/migration_21.rst#_snippet_0

LANGUAGE: python
CODE:
```
stmt = select(column("x", Integer), column("y", String))
```

----------------------------------------

TITLE: Executing SQLAlchemy Statement with Connection (Raw Result) - Python
DESCRIPTION: Demonstrates executing a SQLAlchemy statement using a direct engine connection and fetching results as raw rows. This is typically used for non-ORM results or when bypassing the session. It shows the generated SQL and the fetched data.
SOURCE: https://github.com/sqlalchemy/sqlalchemy/blob/main/doc/build/tutorial/data_select.rst#_snippet_73

LANGUAGE: python
CODE:
```
with engine.connect() as conn:
    result = conn.execute(stmt)
    print(result.all())
```

LANGUAGE: sql
CODE:
```
BEGIN (implicit)
SELECT anon_1.name, address.email_address
FROM address JOIN
  (SELECT user_account.id AS id, user_account.name AS name, user_account.fullname AS fullname
  FROM user_account
  WHERE user_account.name = ?
UNION ALL
  SELECT user_account.id AS id, user_account.name AS name, user_account.fullname AS fullname
  FROM user_account
  WHERE user_account.name = ?) AS anon_1 ON anon_1.id = address.user_id
ORDER BY anon_1.name, address.email_address
[generated in ...] ('sandy', 'spongebob')
ROLLBACK
```

----------------------------------------

TITLE: Performing Bulk Insert with Fixed SQL Expression (SQLAlchemy ORM, Python)
DESCRIPTION: Demonstrates using `session.scalars` with an `insert` statement and `values` to perform a bulk insert. A fixed SQL expression (`func.now()`) is applied to the `timestamp` column for all inserted rows, while row-specific values for `message` are provided in a list passed as the second argument to `session.scalars`.
SOURCE: https://github.com/sqlalchemy/sqlalchemy/blob/main/doc/build/orm/queryguide/dml.rst#_snippet_9

LANGUAGE: python
CODE:
```
from sqlalchemy import func
>>> log_record_result = session.scalars(
...     insert(LogRecord).values(code="SQLA", timestamp=func.now()).returning(LogRecord),
...     [
...         {"message": "log message #1"},
...         {"message": "log message #2"},
...         {"message": "log message #3"},
...         {"message": "log message #4"},
...     ],
... )
```

----------------------------------------

TITLE: Building Select Statement (2.0 Style) - SQLAlchemy Python
DESCRIPTION: Shows the recommended SQLAlchemy 2.0 way to build a `SELECT` statement. Columns are passed positionally, and filtering is done using the `.where()` method, promoting method chaining. This is the preferred pattern moving forward.
SOURCE: https://github.com/sqlalchemy/sqlalchemy/blob/main/doc/build/errors.rst#_snippet_43

LANGUAGE: Python
CODE:
```
stmt = select(table1.c.myid).where(table1.c.myid == table2.c.otherid)
```

----------------------------------------

TITLE: Defining Single Column ForeignKey - Python
DESCRIPTION: This snippet demonstrates how to define a single-column foreign key constraint within a table definition using the ForeignKey object. The ForeignKey specifies that the 'user_id' column in the 'user_preference' table must reference the 'user_id' column in the 'user' table. This is the most common method for single-column foreign keys.
SOURCE: https://github.com/sqlalchemy/sqlalchemy/blob/main/doc/build/core/constraints.rst#_snippet_0

LANGUAGE: python
CODE:
```
user_preference = Table(
    "user_preference",
    metadata_obj,
    Column("pref_id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("user.user_id"), nullable=False),
    Column("pref_name", String(40), nullable=False),
    Column("pref_value", String(100)),
)
```

----------------------------------------

TITLE: Migrating to SQLAlchemy 2.0 Execution Styles (Python)
DESCRIPTION: Demonstrates the SQLAlchemy 2.0 style for database interaction. It shows how to create an engine, execute DDL and DML within a transaction using `connection.execute` and the `text()` construct, and execute a select statement using the updated `select()` syntax with `connection.execute`. This replaces the legacy `engine.execute` calls.
SOURCE: https://github.com/sqlalchemy/sqlalchemy/blob/main/doc/build/changelog/migration_20.rst#_snippet_2

LANGUAGE: python
CODE:
```
from sqlalchemy import column
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy import table
from sqlalchemy import text


engine = create_engine("sqlite://")

# don't rely on autocommit for DML and DDL
with engine.begin() as connection:
    # use connection.execute(), not engine.execute()
    # use the text() construct to execute textual SQL
    connection.execute(text("CREATE TABLE foo (id integer)"))
    connection.execute(text("INSERT INTO foo (id) VALUES (1)"))


foo = table("foo", column("id"))

with engine.connect() as connection:
    # use connection.execute(), not engine.execute()
    # select() now accepts column / table expressions positionally
    result = connection.execute(select(foo.c.id))

    print(result.fetchall())
```

----------------------------------------

TITLE: Setting Up SQLAlchemy Declarative Base and Imports - Python
DESCRIPTION: This snippet provides the necessary imports and defines a base class for Declarative mapping. It includes standard library imports for typing and SQLAlchemy ORM components required for defining mapped classes and relationships.
SOURCE: https://github.com/sqlalchemy/sqlalchemy/blob/main/doc/build/orm/basic_relationships.rst#_snippet_0

LANGUAGE: Python
CODE:
```
from __future__ import annotations
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass
```

----------------------------------------

TITLE: Creating SQLAlchemy Core INSERT Statement with Values
DESCRIPTION: Demonstrates how to construct a basic SQL INSERT statement using the `sqlalchemy.insert` function and specifying column values using the `.values()` method. This creates an `Insert` object representing the statement.
SOURCE: https://github.com/sqlalchemy/sqlalchemy/blob/main/doc/build/tutorial/data_insert.rst#_snippet_0

LANGUAGE: Python
CODE:
```
from sqlalchemy import insert
stmt = insert(user_table).values(name="spongebob", fullname="Spongebob Squarepants")
```

----------------------------------------

TITLE: Loading Object from SQLAlchemy Session
DESCRIPTION: Illustrates how to retrieve an object (`User`) from the database using a SQLAlchemy `Session`. The example uses the `select` construct to build a query filtering by the `User.name` attribute and fetches the first result using `scalars()` and `first()`. It's important to note that this process of loading data from the database does not invoke the class's `__init__` method.
SOURCE: https://github.com/sqlalchemy/sqlalchemy/blob/main/doc/build/orm/mapping_styles.rst#_snippet_6

LANGUAGE: Python
CODE:
```
u1 = session.scalars(select(User).where(User.name == "some name")).first()
```

----------------------------------------

TITLE: Defining ORM Models with DeclarativeBase Subclasses (SQLAlchemy, Python)
DESCRIPTION: Provides a comprehensive example of defining SQLAlchemy ORM models (`User`, `Address`) by subclassing a `DeclarativeBase`. It illustrates how to specify table names (`__tablename__`), columns (`mapped_column`, `Mapped` annotation), and relationships (`relationship`).
SOURCE: https://github.com/sqlalchemy/sqlalchemy/blob/main/doc/build/orm/declarative_styles.rst#_snippet_2

LANGUAGE: Python
CODE:
```
from datetime import datetime
from typing import List
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy import func
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    id = mapped_column(Integer, primary_key=True)
    name: Mapped[str]
    fullname: Mapped[Optional[str]]
    nickname: Mapped[Optional[str]] = mapped_column(String(64))
    create_date: Mapped[datetime] = mapped_column(insert_default=func.now())

    addresses: Mapped[List["Address"]] = relationship(back_populates="user")


class Address(Base):
    __tablename__ = "address"

    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(ForeignKey("user.id"))
    email_address: Mapped[str]

    user: Mapped["User"] = relationship(back_populates="addresses")
```

----------------------------------------

TITLE: Creating and Using Session with sessionmaker Factory - SQLAlchemy ORM - Python
DESCRIPTION: Illustrates how to use sqlalchemy.orm.sessionmaker to create a factory for Session objects bound to a specific engine. This factory can then be used to create sessions within a with block, followed by an explicit session.commit().
SOURCE: https://github.com/sqlalchemy/sqlalchemy/blob/main/doc/build/orm/session_basics.rst#_snippet_4

LANGUAGE: Python
CODE:
```
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# an Engine, which the Session will use for connection
# resources, typically in module scope
engine = create_engine("postgresql+psycopg2://scott:tiger@localhost/")

# a sessionmaker(), also in the same scope as the engine
Session = sessionmaker(engine)

# we can now construct a Session() without needing to pass the
# engine each time
with Session() as session:
    session.add(some_object)
    session.add(some_other_object)
    session.commit()
# closes the session
```

----------------------------------------

TITLE: Defining ORM Models - SQLAlchemy - Python
DESCRIPTION: Defines `User` and `Address` classes mapped to database tables "user" and "address". Includes primary keys, columns, and a one-to-many relationship between User and Address using `relationship` and `ForeignKey`. These models serve as canonical examples for demonstrating session operations.
SOURCE: https://github.com/sqlalchemy/sqlalchemy/blob/main/doc/build/orm/session_state_management.rst#_snippet_8

LANGUAGE: Python
CODE:
```
class User(Base):
    __tablename__ = "user"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(50), nullable=False)
    addresses = relationship("Address", backref="user")


class Address(Base):
    __tablename__ = "address"

    id = mapped_column(Integer, primary_key=True)
    email_address = mapped_column(String(50), nullable=False)
    user_id = mapped_column(Integer, ForeignKey("user.id"), nullable=False)
```

----------------------------------------

TITLE: Handling Duplicate PK with Savepoint - Python
DESCRIPTION: This Python snippet demonstrates the recommended pattern for handling potential primary key conflicts consistently using a nested transaction (savepoint) and catching the IntegrityError. This approach works regardless of whether the conflicting object is already present in the session.
SOURCE: https://github.com/sqlalchemy/sqlalchemy/blob/main/doc/build/changelog/migration_14.rst#_snippet_78

LANGUAGE: python
CODE:
```
# add another Product with same primary key
try:
    with session.begin_nested():
        session.add(Product(id=1))
except exc.IntegrityError:
    print("row already exists")
```

----------------------------------------

TITLE: Creating PostgreSQL Engine using URL String - Python
DESCRIPTION: Demonstrates creating a SQLAlchemy Engine instance connected to a PostgreSQL database using the psycopg2 driver. The connection details are provided directly in a standard database URL string format.
SOURCE: https://github.com/sqlalchemy/sqlalchemy/blob/main/doc/build/core/engines.rst#_snippet_0

LANGUAGE: Python
CODE:
```
from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2://scott:tiger@localhost:5432/mydatabase")
```

----------------------------------------

TITLE: Defining Bidirectional One-to-Many / Many-to-One (Annotated Declarative) - Python
DESCRIPTION: This example shows a bidirectional One-to-Many (Parent to Children) and Many-to-One (Child to Parent) relationship using the modern annotated Declarative style. The relationship targets and collection types are inferred from the Mapped annotation, and back_populates links the two sides.
SOURCE: https://github.com/sqlalchemy/sqlalchemy/blob/main/doc/build/orm/basic_relationships.rst#_snippet_1

LANGUAGE: Python
CODE:
```
class Parent(Base):
    __tablename__ = "parent_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    children: Mapped[List["Child"]] = relationship(back_populates="parent")


class Child(Base):
    __tablename__ = "child_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey("parent_table.id"))
    parent: Mapped["Parent"] = relationship(back_populates="children")
```

----------------------------------------

TITLE: Creating Database Tables via Metadata - Python
DESCRIPTION: This snippet executes the DDL statements required to create the database tables defined by the ORM models. It calls the `create_all()` method on the `MetaData` object associated with the declarative `Base`, using the previously created engine to connect to the database and generate the schema.
SOURCE: https://github.com/sqlalchemy/sqlalchemy/blob/main/doc/build/orm/quickstart.rst#_snippet_2

LANGUAGE: Python
CODE:
```
Base.metadata.create_all(engine)
```

----------------------------------------

TITLE: Defining SQLAlchemy ORM Models - Python
DESCRIPTION: This snippet defines the database schema and corresponding Python object models using SQLAlchemy's Declarative ORM. It includes the base class `Base`, a `User` model mapping to the `user_account` table, and an `Address` model mapping to the `address` table, demonstrating column definitions, primary/foreign keys, and one-to-many relationships.
SOURCE: https://github.com/sqlalchemy/sqlalchemy/blob/main/doc/build/orm/quickstart.rst#_snippet_0

LANGUAGE: Python
CODE:
```
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]

    addresses: Mapped[List["Address"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

class Address(Base):
    __tablename__ = "address"

    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))

    user: Mapped["User"] = relationship(back_populates="addresses")

    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"
```

----------------------------------------

TITLE: Executing SQL and Committing with SQLAlchemy Engine Connection
DESCRIPTION: Shows how to establish a connection using engine.connect(), execute a SQL statement using conn.execute(), and explicitly commit the transaction using conn.commit(). This illustrates the "commit-as-you-go" pattern in the new Engine/Connection API.
SOURCE: https://github.com/sqlalchemy/sqlalchemy/blob/main/doc/build/changelog/migration_20.rst#_snippet_4

LANGUAGE: Python
CODE:
```
from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2:///")

with engine.connect() as conn:
    conn.execute(text("insert into table (x) values (:some_x)"), {"some_x": 10})

    conn.commit()  # commit as you go
```

----------------------------------------

TITLE: Applying Reusable Annotated Column Types to a SQLAlchemy Model
DESCRIPTION: This snippet demonstrates how the previously defined `Annotated` types (`intpk`, `required_name`, `timestamp`) are directly used within `Mapped` annotations in a SQLAlchemy Declarative model. Declarative unpacks these `Annotated` objects, applying their pre-configured `mapped_column` settings to the respective attributes.
SOURCE: https://github.com/sqlalchemy/sqlalchemy/blob/main/doc/build/orm/declarative_tables.rst#_snippet_38

LANGUAGE: Python
CODE:
```
class Base(DeclarativeBase):
    pass


class SomeClass(Base):
    __tablename__ = "some_table"

    id: Mapped[intpk]
    name: Mapped[required_name]
    created_at: Mapped[timestamp]
```

----------------------------------------

TITLE: Using SQLAlchemy ORM Session as Context Manager
DESCRIPTION: Illustrates the use of sqlalchemy.orm.Session as a context manager. It shows creating a session, adding an object, and committing the transaction within the with block. The context manager handles closing the session.
SOURCE: https://github.com/sqlalchemy/sqlalchemy/blob/main/doc/build/changelog/migration_20.rst#_snippet_5

LANGUAGE: Python
CODE:
```
from sqlalchemy.orm import Session

with Session(engine) as session:
    session.add(MyObject())
    session.commit()
```

----------------------------------------

TITLE: Using SQLAlchemy Select and Subquery with Join (Correct)
DESCRIPTION: Demonstrates the recommended SQLAlchemy 2.0 style for creating a subquery from a select statement and then joining another table to that subquery. It shows how to explicitly create the subquery using `.subquery()` before referencing it in the join.
SOURCE: https://github.com/sqlalchemy/sqlalchemy/blob/main/doc/build/changelog/migration_14.rst#_snippet_10

LANGUAGE: Python
CODE:
```
sq1 = select(user.c.id, user.c.name).subquery()
stmt2 = select(addresses, sq1).select_from(addresses.join(sq1))
```

----------------------------------------

TITLE: Managing SQLAlchemy ORM Session Scope with Context Manager
DESCRIPTION: Shows the recommended pattern for managing the lifecycle (scope) of an ORM Session itself using the Session constructor as a context manager. The session is automatically closed upon exiting the `with` block, ensuring resources are released.
SOURCE: https://github.com/sqlalchemy/sqlalchemy/blob/main/doc/build/orm/session_transaction.rst#_snippet_4

LANGUAGE: Python
CODE:
```
with Session(engine) as session:
    session.add(some_object())
    session.add(some_other_object())

    session.commit()  # commits

    session.add(still_another_object)
    session.flush()  # flush still_another_object

    session.commit()  # commits

    result = session.execute(text("<some SELECT statement>"))
```

----------------------------------------

TITLE: Creating SQLAlchemy Engine - Python
DESCRIPTION: This snippet demonstrates how to create a SQLAlchemy Engine instance, which acts as a factory for database connections. It configures the engine to connect to an in-memory SQLite database and enables SQL logging via `echo=True` for demonstration purposes.
SOURCE: https://github.com/sqlalchemy/sqlalchemy/blob/main/doc/build/orm/quickstart.rst#_snippet_1

LANGUAGE: Python
CODE:
```
from sqlalchemy import create_engine
engine = create_engine("sqlite://", echo=True)
```

----------------------------------------

TITLE: Updating Objects with Core Update via Session.execute
DESCRIPTION: Shows the recommended way to perform an UPDATE operation on mapped objects in SQLAlchemy 2.0 using the Core update() construct in conjunction with Session.execute(). This aligns ORM updates with Core statement execution.
SOURCE: https://github.com/sqlalchemy/sqlalchemy/blob/main/doc/build/changelog/migration_20.rst#_snippet_54

LANGUAGE: Python
CODE:
```
session.execute(
  update(User)
  .where(User.name == "foo")
  .values(fullname="Foo Bar")
  .execution_options(
    synchronize_session="evaluate"
  )
)
```

----------------------------------------

TITLE: Defining Declarative Mapped Properties - Declarative Table
DESCRIPTION: This snippet shows how to define ORM mapped properties directly within a declarative class that also defines its `__tablename__`. It demonstrates mapping columns using `mapped_column`, creating relationships with `relationship`, and defining SQL expressions using `column_property`, including type annotations for Mapped attributes.
SOURCE: https://github.com/sqlalchemy/sqlalchemy/blob/main/doc/build/orm/declarative_config.rst#_snippet_0

LANGUAGE: Python
CODE:
```
from typing import List
from typing import Optional

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import column_property
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    firstname: Mapped[str] = mapped_column(String(50))
    lastname: Mapped[str] = mapped_column(String(50))
    fullname: Mapped[str] = column_property(firstname + " " + lastname)

    addresses: Mapped[List["Address"]] = relationship(back_populates="user")


class Address(Base):
    __tablename__ = "address"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    email_address: Mapped[str]
    address_statistics: Mapped[Optional[str]] = mapped_column(Text, deferred=True)

    user: Mapped["User"] = relationship(back_populates="addresses")
```

----------------------------------------

TITLE: Installing SQLAlchemy via pip (Shell)
DESCRIPTION: This command demonstrates the standard method for installing the latest released version of the SQLAlchemy library from PyPI using the pip package manager.
SOURCE: https://github.com/sqlalchemy/sqlalchemy/blob/main/doc/build/intro.rst#_snippet_0

LANGUAGE: text
CODE:
```
pip install sqlalchemy
```

----------------------------------------

TITLE: SQLAlchemy: 2.0 Recommended 'Begin Once' Transaction
DESCRIPTION: Shows the recommended SQLAlchemy 2.0 pattern for executing statements within a single transaction block per connection checkout using `engine.begin()`, suitable for operations that should either fully succeed or fail.
SOURCE: https://github.com/sqlalchemy/sqlalchemy/blob/main/doc/build/changelog/migration_20.rst#_snippet_22

LANGUAGE: Python
CODE:
```
# one choice - work with explicit connection, explicit transaction
# (there remain a few variants on how to demarcate the transaction)

# "begin once" - one transaction only per checkout
with engine.begin() as conn:
    result = conn.execute(stmt)
```

----------------------------------------

TITLE: Setting up SQLAlchemy Database and Seeding Data in Python
DESCRIPTION: This snippet demonstrates how to set up an in-memory SQLite database using the defined ORM models. It creates an engine, generates the database schema based on the model metadata, establishes a connection and session, adds sample User and Address data, and commits the transaction to populate the database. This setup provides the necessary database state for querying examples.
SOURCE: https://github.com/sqlalchemy/sqlalchemy/blob/main/doc/build/orm/queryguide/_plain_setup.rst#_snippet_1

LANGUAGE: python
CODE:
```
engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
Base.metadata.create_all(engine)
conn = engine.connect()
session = Session(conn)
session.add_all(
    [
        User(
            name="spongebob",
            fullname="Spongebob Squarepants",
            addresses=[Address(email_address="spongebob@sqlalchemy.org")],
        ),
        User(
            name="sandy",
            fullname="Sandy Cheeks",
            addresses=[
                Address(email_address="sandy@sqlalchemy.org"),
                Address(email_address="squirrel@squirrelpower.org"),
            ],
        ),
        User(
            name="patrick",
            fullname="Patrick Star",
            addresses=[Address(email_address="pat999@aol.com")],
        ),
        User(
            name="squidward",
            fullname="Squidward Tentacles",
            addresses=[Address(email_address="stentcl@sqlalchemy.org")],
        ),
        User(name="ehkrabs", fullname="Eugene H. Krabs"),
    ]
)
session.commit()
conn.begin()
```