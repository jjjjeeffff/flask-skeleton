# -*- coding: utf-8 -*-
"""
    skeleton.tests.test_models
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Model testing

    :copyright: (c) 2012 by Jeff Long
"""
from skeleton.models.user import User
from nose.tools import assert_equal, assert_not_equal


class TestUser(object):
    """Test User() and methods"""
    @classmethod
    def setup_class(klass):
        """This method is run once for each class before any tests are run"""

    @classmethod
    def teardown_class(klass):
        """This method is run once for each class _after_ all tests are run"""

    def setUp(self):
        """This method is run once before _each_ test method is executed"""

    def teardown(self):
        """This method is run once after _each_ test method is executed"""

    def test_init(self):
        user = User()
        assert_not_equal(user.get_id(), 0)
        assert_equal(user.is_authenticated(), True)
        assert_equal(user.is_active(), True)
        assert_equal(user.is_anonymous(), False)
        assert_not_equal(user.__repr__(), None)

    def test_return_true(self):
        pass

    def test_raise_exc(self):
        pass
