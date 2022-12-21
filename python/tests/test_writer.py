import pytest as pt

from sql.writer import PostgresqlJsonWriter


class TestPostgresqlJsonWriter:
    @pt.fixture
    def writer(self, mocker):
        connection = mocker.stub(name="connection_stub")
        return PostgresqlJsonWriter(connection)

    @pt.fixture
    def schema(self):
        return ""

    @pt.fixture
    def table(self):
        return ""

    @pt.fixture
    def data(self):
        return ""

    def test_bulk_write(self, writer, mocker, schema, table, data):
        mocker.patch.object(writer, "_connection")
        writer._connection.execute.__enter__.return_value = None
        writer.bulk_write(schema, table, data)
        writer._connection.execute.assert_called_once()
