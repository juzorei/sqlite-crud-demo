import sqlite3
import pytest
from repository import Items, InvalidItem

def test_sqlite_crud_validation_and_parameterized_queries():
    connection = sqlite3.connect(":memory:")
    items = Items(connection)
    first = items.create("Robert'); DROP TABLE items;--", "literal text")
    assert items.get(first)["description"] == "literal text"
    items.update(first, "Revised", "New")
    assert items.list() == [{"id":first,"name":"Revised","description":"New"}]
    assert items.delete(first)
    assert not items.delete(first)
    with pytest.raises(InvalidItem):
        items.create(" ", "x")
    connection.close()
