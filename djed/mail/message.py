from pyramid.renderers import render
from pyramid_mailer.message import (
    Attachment,
    Message,
)

class MessageTemplate(Message):

    template = None

    def __init__(self, request, **kwargs):
        super(MessageTemplate, self).__init__()
        self.__dict__.update(kwargs)

        self.request = request
        self.settings = request.registry.settings

    def render(self):
        return render(self.template, self.__dict__, self.request)

    def update(self):
        if not self.sender:
            self.sender = self.settings['mail.default_sender']

    def send(self, recipients=None, mailer=None):

        if recipients:
            self.recipients = recipients

        self.update()

        if self.template:
            self.body = self.render()

        if mailer is None:
            mailer = self.request.get_mailer()

        if mailer is not None:
            mailer.send(self)

