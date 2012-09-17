# -*- coding: utf-8 -*-
"""
    skeleton.tests.test_misc
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Misc. functionality testing

    :copyright: (c) 2012 by Jeff Long
"""
import skeleton


class TestMisc(object):

    @classmethod
    def setup_class(klass):
        """This method is run once for each class before any tests are run"""
        skeleton.app.config.from_object('skeleton.config.TestingConfig')
        from skeleton import mail
        klass.app = skeleton.app.test_client()

    @classmethod
    def teardown_class(klass):
        """This method is run once for each class _after_ all tests are run"""

    def setUp(self):
        """This method is run once before _each_ test method is executed"""

    def teardown(self):
        """This method is run once after _each_ test method is executed"""

    def test_mail(self):
        '''Testing mail with no templates'''
        skeleton.mail.send('no_template', 'Test Subject', ['test@test.com'])
