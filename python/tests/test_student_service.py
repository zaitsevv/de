import pytest as pt

from service import StudentService


class TestStudentService:
    @pt.fixture
    def student_service(self, mocker):
        writer = mocker.stub(name="writer_stub")
        schema = ""
        students_table = ""
        return StudentService(writer, schema, students_table)

    def test_write_json_array(self, student_service, mocker, tmp_path):
        path = tmp_path / "empty"
        path.touch()
        mocker.patch.object(student_service, "_writer")
        student_service.write_json_array(str(path))
        student_service._writer.bulk_write.assert_called_once()
