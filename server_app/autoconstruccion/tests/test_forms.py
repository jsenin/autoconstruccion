import unittest
from autoconstruccion import create_app
from autoconstruccion.forms import ProjectForm


# Project name should not be empty
# Project name should has at least 3 character
# Project description should not be empty


class TestProject(unittest.TestCase):

    def setUp(self):
        self.app = create_app()

    def test_should_throw_exception_when_is_empty(self):
        fixture = {}
        project = ProjectForm(data=fixture)
        project.validate()
        assert project.validate() == False

    def test_should_fail_if_name_is_empty(self):
        fixture = {'name': ''}
        project = ProjectForm(data=fixture)
        project.validate()
        assert 'name' in project.errors
        assert 'This field is required.' in project.errors['name']

    def test_should_fail_if_name_has_less_than_3_chars(self):
        fixture = {'name': 'no'}
        project = ProjectForm(data=fixture)
        project.validate()
        assert 'name' in project.errors
        assert 'Field must be between 3 and 255 characters long.' \
            in project.errors['name']

    def test_should_fail_if_description_is_empty(self):
        fixture = {'description': ''}
        project = ProjectForm(data=fixture)
        project.validate()
        assert 'description' in project.errors
        assert 'Field must be at least 5 characters long.' \
            in project.errors['description']


if __name__ == '__main__':
    unittest.main()
