# SQLite CRUD demo

A small data layer with validated inputs and parameterized SQL. This is a
standalone demonstration, not an HTTP server or a delivered client project.

```powershell
py -3 -X utf8 -m pip install -e '.[dev]'
py -3 -X utf8 -m pytest -q
```

```python
import sqlite3
from repository import Items

connection = sqlite3.connect(":memory:")
items = Items(connection)
item_id = items.create("Tea", "Sample item")
print(items.get(item_id))
items.update(item_id, "Green tea", "Updated item")
items.delete(item_id)
connection.close()
```

The caller owns the connection. Writes commit through SQLite transactions.
Names must be nonempty and at most 200 characters; descriptions are limited to
10,000 characters. Missing IDs return `None` or `False`. Tests include an SQL
injection-shaped name treated as literal data. Authentication, HTTP routing,
schema versioning and multi-user permissions are outside this demo.
