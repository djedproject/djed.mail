import logging
from email.utils import formataddr

from pyramid_mailer import get_mailer
from pyramid_mailer.mailer import (
    DummyMailer,
    Mailer,
)
from pyramid_mailer.interfaces import IMailer

from djed.mail.message import (
    Attachment,
    Message,
    MessageTemplate,
)


log = logging.getLogger('djed.mail')


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
    
