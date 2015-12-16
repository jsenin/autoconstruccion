import requests
import smtplib


class NotifierFactory:

    @staticmethod
    def factory(options):

        if (not type(options) is dict):
            options = {}

        transport = options.get('transport', '')
        transport = str.upper(transport)

        if (transport == 'MAILGUN'):
            return MailgunTransport(options)

        if (transport == 'SENDMAIL'):
            return SendmailTransport(options)

        return FooTransport(options)


class MailTransport:

    def send(self, options):
        pass


class FooTransport(MailTransport):
    def __init__(self, config):
        pass


class SendmailTransport(MailTransport):
    def __init__(self, config):
        self.config = config

    def validate(self, **options):
        if (not options.get('to')):
            raise KeyError('to not found')

        if (not options.get('subject')):
            raise KeyError('subject not found')

        if (not options.get('text')):
            raise KeyError('text not found')

    def send(self, **options):
        self.validate(**options)
        config = self.config

        server = smtplib.SMTP(config.get('host'), config.get('port'))
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(config.get('login'), config.get('password'))
        msg = "\r\n".join([
            "Subject: %s" % options.get('subject'),
            "",
            options.get('text')
        ])
        server.sendmail(config.get('from'), options.get('to'), msg)


class MailgunTransport(MailTransport):

    def __init__(self, config):
        if (not config.get('api-key')):
            raise KeyError('api-key not found')

        if (not config.get('host')):
            raise KeyError('host not found')

        self.config = config

    def validate(self, **options):
        if (not options.get('to')):
            raise KeyError('to not found')

        if (not options.get('subject')):
            raise KeyError('subject not found')

        if (not options.get('text')):
            raise KeyError('text not found')

    def send(self, **options):
        self.validate(**options)
        config = self.config

        return requests.post(
            config.get('host'),
            auth=("api", config.get('api-key')),
            data={
                "from": config.get('from'),
                "to":  options.get('to'),
                "subject": options.get('subject'),
                "text": options.get('text')})
