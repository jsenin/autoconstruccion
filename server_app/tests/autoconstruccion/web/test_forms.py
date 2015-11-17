import pytest
from autoconstruccion.web.forms import ProjectForm


# # define app fixture for pytest-flask
# @pytest.fixture()
# def app():
#     from autoconstruccion import create_app, db
#     # for now we test over sqlite in memory, so no empty db needed
#     test_app = create_app('TESTING_MEMORY')
#     db.init_app(test_app)
#     with test_app.test_request_context():
#         db.create_all()
#     return test_app


# ----- Test ProjectForm -----

# creates a fixture that returns a valid form
@pytest.fixture()
def project_form():
    """
    Returns a Project Form with valid data populated.
    """
    values = {'name': "Proyecto de testing",
              'description': "Este es un proyecto de prueba para test",
              'start_date': "24-01-2015",
              'end_date': "24-02-2015",
              'location': "Prueba a ver si lo encuentras",
              'contact_phone': "987654321",
              'image': None
              }
    return ProjectForm(data=values)


def test_get_valid_project_form(project_form):
    validity = project_form.validate()
    assert validity


def test_should_throw_exception_when_is_empty(project_form):
    fixture = {}
    project = ProjectForm(data=fixture)
    assert not project.validate()


# ------ Test name field
def test_should_fail_if_name_is_empty(project_form):
    project_form.name.data = None
    assert not project_form.validate()
    project_form.name.data = ''
    assert not project_form.validate()
    # test if error message appears
    assert 'name' in project_form.errors


def test_should_be_ok_when_name_has_5_chars(project_form):
    project_form.name.data = 'Peter'
    assert project_form.name.validate(project_form)


def test_should_fail_if_name_has_less_than_3_chars(project_form):
    project_form.name.data = 'Dr'
    assert not project_form.validate()
    assert 'name' in project_form.errors


# ------ Test description field
def test_should_fail_if_description_is_empty(project_form):
    project_form.description.data = None
    assert not project_form.validate()
    project_form.description.data = ''
    assert not project_form.validate()
    assert 'description' in project_form.errors


def test_should_accept_description_greater_than_5(project_form):
    project_form.description.data = 'description'
    assert project_form.validate()


def test_should_fail_if_description_has_less_than_5_characters(project_form):
    project_form.description.data = 'desc'
    assert not project_form.validate()




if __name__ == '__main__':
    pytest.main()
