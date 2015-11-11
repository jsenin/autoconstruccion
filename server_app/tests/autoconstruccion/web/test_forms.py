import unittest

from autoconstruccion import create_app
from autoconstruccion.web.forms import ProjectForm


class TestProject(unittest.TestCase):

    def setUp(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.app_context().push()

    def test_should_throw_exception_when_is_empty(self):
        fixture = {}
        project = ProjectForm(data=fixture)
        assert not project.validate()

    def test_should_be_ok_when_name_has_5_chars(self):
        fixture = {'name': 'Peter'}
        project = ProjectForm(data=fixture)
        assert project.name.validate(project)

    def test_should_fail_if_name_is_empty(self):
        fixture = {'name': ''}
        project = ProjectForm(data=fixture)
        assert not project.name.validate(project)
        assert 'name' in project.errors
        assert 'This field is required.' in project.errors['name']

    def test_should_fail_if_name_has_less_than_3_chars(self):
        fixture = {'name': 'no'}
        project = ProjectForm(data=fixture)
        assert not project.name.validate(project)
        assert 'name' in project.errors
        assert 'Field must be between 3 and 255 characters long.' \
            in project.errors['name']

    def test_should_accept_description_greater_than_5(self):
        fixture = {'description': 'description'}
        project = ProjectForm(data=fixture)
        assert project.description.validate(project)

    def test_should_fail_if_description_is_empty(self):
        fixture = {'description': ''}
        project = ProjectForm(data=fixture)
        assert not project.description.validate(project)
        assert 'description' in project.errors
        assert 'Field must be at least 5 characters long.' \
            in project.errors['description']

if __name__ == '__main__':
    unittest.main()
