import logging
from email.utils import (
    formataddr,
    parseaddr,
)

from pyramid.renderers import render

from pyramid_mailer import get_mailer
from pyramid_mailer.interfaces import IMailer
from pyramid_mailer.mailer import (
    DummyMailer,
    Mailer,
)
from pyramid_mailer.message import (
    Attachment,
    Message,
)


log = logging.getLogger('djed.mail')


class MailTemplate(Message):

    template = None

    def __init__(self, request, **kwargs):
        super(MailTemplate, self).__init__()

        self.__dict__.update(kwargs)

        self.request = request
        self.settings = request.registry.settings

        if self.sender is None:
            self.sender = self.settings['mail.default_sender']

    def render(self):
        return render(self.template, self.__dict__, self.request)

    def update(self):
        pass

    def send(self, recipients=None, mailer=None):

        self.update()

        if recipients is not None:
            self.recipients = recipients

        if self.template is not None:
            self.body = self.render()

        if mailer is None:
            mailer = self.request.get_mailer()

        if mailer is not None:
            mailer.send(self)


def init_mailer(config, mailer=None):

    settings = config.registry.settings
    settings['mail.default_sender'] = settings.get('mail.default_sender',
        formataddr(('Site administrator', 'admin@localhost')))

    if not mailer:
        mailer = Mailer.from_settings(settings)

    config.registry.registerUtility(mailer, IMailer)
    
    log.info("Initialize mailer")


def includeme(config):
    config.include('pyramid_tm')

    config.add_directive('init_mailer', init_mailer)
    config.add_request_method(get_mailer, 'get_mailer')
