from djed.testing import BaseTestCase


#class Content(object):
#    pass


class TestMailer(BaseTestCase):

    _includes = ('djed.mail', 'pyramid_chameleon')

    def test_init_mailer(self):
        from djed.mail import Mailer

        self.config.init_mailer()

        mailer = self.request.get_mailer()

        self.assertIsInstance(mailer, Mailer)

    def test_custom_mailer(self):
        from djed.mail import DummyMailer

        self.config.init_mailer(DummyMailer())

        mailer = self.request.get_mailer()

        self.assertIsInstance(mailer, DummyMailer)


class TestMailTemplate(BaseTestCase):

    _includes = ('djed.mail', 'pyramid_chameleon')

    def _init_dummy_mailer(self):
        from djed.mail import DummyMailer

        self.config.init_mailer(DummyMailer())

    def _make_one(self):
        from djed.mail import MailTemplate

        class Template(MailTemplate):

            template = 'tests:test_mail_tmpl.pt'

        return Template
        
    def test_ctor(self):

        self._init_dummy_mailer()

        cls = self._make_one()
        tmpl = cls(self.request, testattr='testattr')

        self.assertEqual(tmpl.testattr, 'testattr')

    def test_render(self):

        self._init_dummy_mailer()

        cls = self._make_one()

        tmpl = cls(self.request, name='world')

        self.assertEqual(tmpl.render(), 'Hello world\n')

    def test_sender(self):

        self._init_dummy_mailer()

        cls = self._make_one()

        tmpl = cls(self.request)

        self.assertEqual(tmpl.sender, self.registry.settings['mail.default_sender'])

        tmpl = cls(self.request, sender='test@simiaproject.org')

        self.assertEqual(tmpl.sender, 'test@simiaproject.org')

    def test_send(self):

        self._init_dummy_mailer()

        cls = self._make_one()
        tmpl = cls(self.request,
                   recipients=['test@simiaproject.org'],
                   name='world')

        mailer = self.request.get_mailer()
        data = mailer.outbox

        tmpl.send()

        msg = data[0]

        self.assertEqual(
            msg.sender, 'Site administrator <admin@localhost>')
        self.assertEqual(
            msg.recipients, ['test@simiaproject.org'])
        self.assertIn('From: Site administrator <admin@localhost>',
                      msg.to_message().as_string())

        tmpl.send(recipients=['test2@simiaproject.org'])

        msg = data[1]
        self.assertEqual(msg.recipients, ['test2@simiaproject.org'])

    def test_no_template(self):

        self._init_dummy_mailer()

        cls = self._make_one()
        tmpl = cls(self.request, body='Hello', template=None,
                   recipients=['test@simiaproject.org'])

        mailer = self.request.get_mailer()

        tmpl.send()

        msg = mailer.outbox[0]

        self.assertIn('Hello', msg.to_message().as_string())
