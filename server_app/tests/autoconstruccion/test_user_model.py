import unittest

from autoconstruccion import create_app
from autoconstruccion.web.forms import UserForm


class TestUserForm(unittest.TestCase):

    def getUser(self):
        user = {
            'full_name': 'joe mallony',
            'email': 'joe@malony.it',
            'phone_number': '912345678',
            'habilities': 'se cocinar pasta',
            'availability': 'todos los dias, no trabajo',
            'tools': 'picos y palas',
            'materials': 'cal y arena',
        }
        return user

    def setUp(self):
        self.fixture = self.getUser()
        app = create_app()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.app_context().push()

    def test_user_valid_must_be_valid(self):
        user = UserForm(data=self.fixture)
        assert user.validate()

    def test_fail_when_full_name_is_empty(self):
        self.fixture['full_name'] = ''
        user = UserForm(data=self.fixture)
        assert not user.full_name.validate(user)

    def test_fail_when_email_is_empty(self):
        self.fixture['email'] = ''
        user = UserForm(data=self.fixture)
        assert not user.email.validate(user)

    def test_fail_when_email_not_compilance(self):
        self.fixture['email'] = 'memememe'
        user = UserForm(data=self.fixture)
        assert not user.email.validate(user)


if __name__ == '__main__':
    unittest.main()
