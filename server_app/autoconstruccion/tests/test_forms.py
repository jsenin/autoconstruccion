import unittest
from autoconstruccion.forms import ProjectForm


class TestProject(unittest.TestCase):

    def test_should_throw_exception_when_is_empty(self):
        fixture = {}
        project = ProjectForm(data=fixture)
        assert not project.validate()

    def test_should_fail_if_name_is_empty(self):
        fixture = {'name': ''}
        project = ProjectForm(data=fixture)
        assert not project.validate()
        assert 'name' in project.errors
        assert 'This field is required.' in project.errors['name']

    def test_should_fail_if_name_has_less_than_3_chars(self):
        fixture = {'name': 'no'}
        project = ProjectForm(data=fixture)
        assert not project.validate()
        assert 'name' in project.errors
        assert 'Field must be between 3 and 255 characters long.' \
            in project.errors['name']

    def test_should_fail_if_description_is_empty(self):
        fixture = {'description': ''}
        project = ProjectForm(data=fixture)
        assert not project.validate()
        assert 'description' in project.errors
        assert 'Field must be at least 5 characters long.' \
            in project.errors['description']


if __name__ == '__main__':
    unittest.main()
