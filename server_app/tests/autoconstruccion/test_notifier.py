import pytest
from autoconstruccion.notifier import NotifierFactory, MailgunTransport, SendmailTransport, FooTransport



# todo :
# clase correo tiene un metodo send mail
# hay varios tipos de envio de correo
# correo debe tener un from, from to , subject, text

@pytest.fixture()
def mail_fixture():
    return {
        'to': 'demo@demo.com',
        'subject': 'demo',
        'text': 'texto de prueba'
    }


@pytest.fixture()
def mailgun_fixture():
    return {
        'transport': 'Mailgun',
        'api-key': '1234',
        'host': 'fofofof',
        'from': 'me@me.com'
    }

@pytest.fixture()
def mailgun_mailer(mailgun_fixture):
    return NotifierFactory.factory(mailgun_fixture)


def test_MailTransport_type_will_be_mailgun_when_its_configured(mail_fixture, mailgun_fixture):
    mailer = NotifierFactory.factory(mailgun_fixture)
    assert isinstance(mailer, MailgunTransport)


def test_MailTransport_type_will_be_sendmail_when_its_configured(mail_fixture):
    config = {'transport': 'Sendmail'}
    mailer = NotifierFactory.factory(config)
    assert isinstance(mailer, SendmailTransport)


def test_MailTransport_type_will_be_footransport_as_fallback(mail_fixture):
    config = {}
    mailer = NotifierFactory.factory(config)
    assert isinstance(mailer, FooTransport)


def test_mailgun_transport_needs_an_api_key(mailgun_fixture):
    config = mailgun_fixture
    del config['api-key']

    with pytest.raises(KeyError) as raise_info:
        NotifierFactory.factory(config)
        assert 'api-key not found' in str(raise_info.value)


def test_mailgun_transport_needs_a_host(mailgun_fixture):
    config = mailgun_fixture
    del config['host']

    with pytest.raises(KeyError) as raise_info:
        NotifierFactory.factory(config)
        assert 'host not found' in str(raise_info.value)


def test_send_with_fixture_is_sent(mail_fixture, mailgun_mailer):
    mailer = mailgun_mailer
    mailer.validate(**mail_fixture)


def test_when_send_a_mail_without_a_dest_must_fail(mail_fixture,mailgun_mailer):

    mailer = mailgun_mailer
    del mail_fixture['to']

    with pytest.raises(KeyError) as raise_info:
        mailer.validate(**mail_fixture)

    assert 'to not found' in str(raise_info.value)

def test_when_send_a_mail_without_a_subject_must_fail(mail_fixture,mailgun_mailer):

    mailer = mailgun_mailer
    del mail_fixture['subject']

    with pytest.raises(KeyError) as raise_info:
        mailer.validate(**mail_fixture)

    assert 'subject not found' in str(raise_info.value)

def test_when_send_a_mail_without_a_text_must_fail(mail_fixture,mailgun_mailer):

    mailer = mailgun_mailer
    del mail_fixture['text']

    with pytest.raises(KeyError) as raise_info:
        mailer.validate(**mail_fixture)

    assert 'text not found' in str(raise_info.value)
