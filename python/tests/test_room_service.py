import pytest as pt

from service import RoomService


class TestRoomService:
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
        """

    @pt.fixture
    def room_service(self, mocker):
        writer = mocker.stub(name="writer_stub")
        reader = mocker.stub(name="reader_stub")
        schema = ""
        rooms_table = ""
        students_table = ""
        return RoomService(writer, reader, schema, rooms_table, students_table)

    def test_fetch_data_template(self, room_service, mocker, expected, tmp_path):
        path = tmp_path / "empty"
        path.mkdir()
        mocker.patch.object(room_service, "_reader")
        room_service._reader.fetch.return_value = expected
        room_service._RoomService__fetch_data_template(
            str(path), "fetch_data_template", ""
        )
        with open(f"{str(path)}/fetch_data_template.unknown") as file:
            actual = file.read()
        assert actual == expected

    def test_write_json_array(self, room_service, mocker, tmp_path):
        path = tmp_path / "empty"
        path.touch()
        mocker.patch.object(room_service, "_writer")
        room_service._writer.bulk_write.return_value = None
        room_service.write_json_array(str(path))
        room_service._writer.bulk_write.assert_called_once()
