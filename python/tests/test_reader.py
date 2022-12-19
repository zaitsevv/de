import pytest as pt

from sql.reader import PostgresqlJsonReader, PostgresqlXmlReader


class TestPostgresqlJsonReader:
    @pt.fixture
    def expected(self):
        return """
[
    {
        "id": 0,
        "name": "Room #0"
    },
    {
        "id": 1,
        "name": "Room #1"
    }
]        
""".strip()

    @pt.fixture
    def data(self):
        return [{"id": 0, "name": "Room #0"}, {"id": 1, "name": "Room #1"}]

    @pt.fixture
    def reader(self, mocker):
        connection = mocker.stub(name="connection_stub")
        return PostgresqlJsonReader(connection)

    @pt.fixture
    def query(self, mocker):
        return mocker.stub(name="query_stub")

    def test_fetch(self, reader, mocker, data, expected, query):
        mocker.patch.object(reader, "_connection")
        reader._connection.execute(query).fetchall.return_value = data
        actual = reader.fetch(query)
        assert actual == expected


class TestPostgresqlXmlReader:
    @pt.fixture
    def expected(self):
        return """
<?xml version="1.0" ?>
<root>
    <item>
        <id>0</id>
        <name>Room #0</name>
    </item>
    <item>
        <id>1</id>
        <name>Room #1</name>
    </item>
</root>
""".lstrip()

    @pt.fixture
    def data(self):
        return [{"id": 0, "name": "Room #0"}, {"id": 1, "name": "Room #1"}]

    @pt.fixture
    def reader(self, mocker):
        connection = mocker.stub(name="connection_stub")
        return PostgresqlXmlReader(connection)

    @pt.fixture
    def query(self, mocker):
        return mocker.stub(name="query_stub")

    def test_fetch(self, reader, mocker, data, expected, query):
        mocker.patch.object(reader, "_connection")
        reader._connection.execute(query).fetchall.return_value = data
        actual = reader.fetch(query)
        assert actual == expected
