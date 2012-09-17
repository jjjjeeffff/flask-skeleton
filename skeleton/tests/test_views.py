# -*- coding: utf-8 -*-
"""
    skeleton.tests.test_views
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    View testing

    :copyright: (c) 2012 by Jeff Long
"""
import skeleton
from werkzeug.security import generate_password_hash


class TestViews(object):
    """Test all the views!"""

    @classmethod
    def setup_class(klass):
        """This method is run once for each class before any tests are run"""
        skeleton.app.config.from_object('skeleton.config.TestingConfig')
        from skeleton import mail
        klass.app = skeleton.app.test_client()

        # Initialize database
        klass.db = skeleton.db
        klass.db.create_all()

        # Create a valid user
        user = skeleton.models.user.User()
        user.id = 1
        user.email = 'testing@test.com'
        user.pwhash = generate_password_hash('testpassword')
        klass.db.session.add(user)
        klass.db.session.commit()

    @classmethod
    def teardown_class(klass):
        """This method is run once for each class _after_ all tests are run"""

    def setUp(self):
        """This method is run once before _each_ test method is executed"""

    def teardown(self):
        """This method is run once after _each_ test method is executed"""

    def test_init(self):
        pass

    def test_default(self):
        '''Testing '/' without TESTING disabled'''
        skeleton.app.config['TESTING'] = False
        self.app.get('/')
        skeleton.app.config['TESTING'] = True

    def test_404(self):
        '''Testing 404 pages'''
        self.app.get('/this/url/does/not/exist')

    def test_user_session(self):
        '''Testing user session (logging in and out)'''

        # Invalid username/password check
        data = dict()
        data['email'] = 'some@invaliduser.com'
        rv = self.app.post('/session', data=data, follow_redirects=True)
        assert 'Invalid e-mail/password' in rv.data

        # Incomplete registration attempt (need to verify e-mail)
        data['email'] = 'testing@test.com'
        rv = self.app.post('/session', data=data, follow_redirects=True)
        assert 'Please check your e-mail' in rv.data

        # Correct attempt
        user_obj = skeleton.models.user.User
        user = user_obj.query.filter(user_obj.id == 1).one()
        user.level = 1
        self.db.session.add(user)
        self.db.session.commit()

        # Invalid password
        data['pass'] = 'incorrect!'
        rv = self.app.post('/session', data=data, follow_redirects=True)
        assert 'Invalid e-mail/password' in rv.data

        # Correct password with redirect and remember
        data['pass'] = 'testpassword'
        data['next'] = '/'
        data['remember'] = 'on'
        rv = self.app.post('/session', data=data, follow_redirects=True)
        assert 'Logout' in rv.data

        # Visit an auth-required page
        rv = self.app.get('/account')
        assert 'Account' in rv.data

        # Logout
        rv = self.app.get('/session/out', follow_redirects=True)
        assert 'Sign in' in rv.data

    def test_account(self):
        '''Testing account creation'''

        # Incomplete registration attempt
        data = dict()
        data['agree'] = 'on'
        rv = self.app.post('/account/create', data=data, follow_redirects=True)
        assert 'Please correct the errors' in rv.data

        # Valid registration
        data['password'] = 'abcdefg12345'
        data['password_confirm'] = 'abcdefg12345'
        data['new_email'] = 'testing2@test.com'
        rv = self.app.post('/account/create', data=data, follow_redirects=True)
        assert 'Account created' in rv.data

        # User already exists error
        data['new_email'] = 'testing@test.com'
        rv = self.app.post('/account/create', data=data, follow_redirects=True)
        assert 'already exists' in rv.data

    def test_email_verification(self):
        '''Testing e-mail verification process'''

        # Test invalid key
        rv = self.app.get('/account/verify/abc')
        assert 'already been validated' in rv.data

        # Test valid key
        meta_obj = skeleton.models.user.UserMeta()
        meta_obj.key = 'email_ver_key'
        meta_obj.val = 'testkey'
        meta_obj.user_id = 1
        self.db.session.add(meta_obj)
        self.db.session.commit()
        rv = self.app.get('/account/verify/testkey', follow_redirects=True)
        assert 'successfully verified' in rv.data

    def test_account_recovery(self):
        rv = self.app.get('/account/recovery')
        assert 'Account Recovery' in rv.data

        # Test blank submit
        rv = self.app.post('/account/recovery')

        # Create existing
        meta_obj = skeleton.models.user.UserMeta()
        meta_obj.key = 'password_rec_key'
        meta_obj.val = 'testkey'
        meta_obj.user_id = 1
        self.db.session.add(meta_obj)
        self.db.session.commit()

        # Test invalid user
        data = {'email': 'test@test.com'}
        rv = self.app.post('/account/recovery', data=data,
                           follow_redirects=True)
        assert 'No user with that' in rv.data

        data = {'email': 'testing@test.com'}
        rv = self.app.post('/account/recovery', data=data,
                           follow_redirects=True)
        assert 'check your e-mail and follow the instructions.' in rv.data

        # Test password reset page (key not checked yet)
        rv = self.app.get('/account/recovery/somekey', follow_redirects=True)
        assert 'Reset Password' in rv.data

        # Test password reset submit (mismatched passwords)
        data = {'password': 'some_pass',
                'password_confirm': 'some_unmatched_pass'}
        rv = self.app.post('/account/recovery/somekey', data=data,
                           follow_redirects=True)
        assert 'Passwords must match' in rv.data

        # Test password reset submit (invalid key checked)
        data = {'password': 'some_pass',
                'password_confirm': 'some_pass'}
        rv = self.app.post('/account/recovery/somekey', data=data,
                           follow_redirects=True)
        assert 'no longer valid' in rv.data

        # Test valid reset
        data = {'password': 'some_pass',
                'password_confirm': 'some_pass'}
        rv = self.app.post('/account/recovery/testkey', data=data,
                           follow_redirects=True)
        assert 'successfully updated' in rv.data
