import unittest

from autoconstruccion import create_app
from autoconstruccion.web.forms import EventForm


class TestEventForm(unittest.TestCase):
    def getEvent(self):
        event = {
            'name': 'Pintar',
            'description': 'Hay que pintar las paredes de un 6 piso',
            'start_date': '24/12/2015'
        }
        return event

    def setUp(self):
        self.fixture = self.getEvent()
        app = create_app()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.app_context().push()

    def test_event_valid_must_be_valid(self):
        event = EventForm(data=self.fixture)
        assert event.validate()

    def test_should_ok_when_name_has_3_letters(self):
        self.fixture['name'] = 'alv'
        event = EventForm(data=self.fixture)
        assert event.name.validate(event)

    def test_should_not_accept_when_there_no_name(self):
        self.fixture['name'] = ''
        event = EventForm(data=self.fixture)
        assert not event.name.validate(event)

    def test_should_ok_when_description_has_3_letters(self):
        self.fixture['description'] = 'des'
        event = EventForm(data=self.fixture)
        assert event.description.validate(event)

    def test_should_not_accept_when_there_no_description(self):
        self.fixture['description'] = ''
        event = EventForm(data=self.fixture)
        assert not event.description.validate(event)
