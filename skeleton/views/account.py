# -*- coding: utf-8 -*-
"""
    skeleton.views.account
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Account management and profile editing.

    :copyright: (c) 2012 by Jeff Long
"""
from flask import Module, redirect, url_for, request, \
    render_template, flash, session
from flask.ext.login import login_required
from werkzeug.security import generate_password_hash
from .. import db
from ..models.user import User, UserMeta
from ..forms.signup import SignupForm
from ..forms.password_reset import PasswordResetForm
from ..mail import send
import random


account = Module(__name__)


@account.route('/account')
@login_required
def index():
    """Account dashboard where a user can edit their user information and
    profile details.
    """
    return render_template('account/index.html')


@account.route('/account/create', methods=['POST'])
def create_account():
    """This checks the create account form for errors and either creates the
    account or flashes an error message. An e-mail is also sent upon account
    creation with the validation key.

    TODO Offload the e-mail sending to Celery.
    """
    form = SignupForm(request.form)
    if request.method == 'POST' and form.validate():
        # Create user
        user = User()
        user.email = form.new_email.data
        user.pwhash = generate_password_hash(form.password.data)
        user.level = 0

        # Generate verification key
        key = str(random.getrandbits(64))
        user.user_meta = [
            UserMeta(key='email_ver_key', val=key)
        ]

        # Send e-mail
        send('email_verification', 'Welcome to your Flask skeleton site!',
             [user.email], user=user, key=key)
        db.session.add(user)

    else:
        flash("Oops! Please correct the errors in the signup form.")
        session['form'] = request.form
        return redirect(url_for('default.index'))
    return redirect(url_for('account.create_account_success'))


@account.route('/welcome')
def create_account_success():
    """This is the page the user sees upon successful account creation. They
    still need to verify their e-mail after this step.
    """
    return render_template('account/welcome.html')


@account.route('/account/verify/<key>')
def verify_email(key):
    """Verifies an e-mail address based on a previously determined key.
    The key is deleted and user's level updated."""
    user_key = UserMeta.query \
        .filter_by(key='email_ver_key') \
        .filter_by(val=key).first()
    if user_key:
        db.session.delete(user_key)
        user_key.user.level = 1
        flash('E-mail address \'%s\' successfully verified! Please \
                login below.' % user_key.user.email)
        return redirect(url_for('default.index'))
    return render_template('/errors/invalid_verification_key.html')


@account.route('/account/recovery')
def account_recovery_request():
    """Present a form for a user to create a new one-time key that will allow
    them to reset their password."""
    return render_template('/account/recovery.html')


@account.route('/account/recovery', methods=['POST'])
def account_key_generator():
    """Process a request for a new password recovery key. If the requested
    e-mail is valid, the key will be e-mailed to the user to generate a
    new password."""
    if not request.form.get('email'):
        return redirect(url_for('account.account_recovery_request'))
    user = User.query.filter_by(email=request.form['email']).first()
    # Check for valid user
    if not user:
        flash('No user with that e-mail address exists, please try again.')
        return redirect(url_for('account.account_recovery_request'))
    # Delete any existing key
    existing_keys = UserMeta.query \
        .filter_by(key='password_rec_key', user_id=user.id)
    if existing_keys:
        for key in existing_keys:
            db.session.delete(key)

    # Generate password recovery key
    key = str(random.getrandbits(128))
    user.user_meta = [
        UserMeta(key='password_rec_key', val=key)
    ]

    # E-mail user
    send('password_recovery', 'Password Recovery',
         [user.email], user=user, key=key)

    flash('All set! Please check your e-mail and follow the instructions.')
    return redirect(url_for('default.index'))


@account.route('/account/recovery/<key>')
def account_recovery(key, form=None):
    """Presents a form for entering a new password."""
    if not form:
        form = PasswordResetForm(request.form)
    return render_template('/account/reset_password.html', key=key, form=form)


@account.route('/account/recovery/<key>', methods=['POST'])
def reset_password(key):
    """Validates the password reset form and provided key, then updates the
    user's password if everything looks good."""
    form = PasswordResetForm(request.form)
    if form.validate():
        pass_key = UserMeta.query.filter_by(key='password_rec_key',
                                            val=key).first()
        if not pass_key:
            flash("Your password reset key is no longer valid, \
                   please try again.")
            return redirect(url_for('default.index'))

        # Update password
        pass_key.user.pwhash = generate_password_hash(form.password.data)

        # Delete used key
        db.session.delete(pass_key)

        flash("Your password has been successfully updated, \
               please login below.")
        return redirect(url_for('default.index'))
    return account_recovery(key, form)
