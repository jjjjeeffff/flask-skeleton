# -*- coding: utf-8 -*-
"""
    skeleton.views.session
    ~~~~~~~~~~~~~~~~~~~~~~

    User login/logout session handling

    :copyright: (c) 2012 by Jeff Long
"""


from flask import Module, redirect, url_for, request, flash
from skeleton.models.user import User
from werkzeug.security import check_password_hash
from flask.ext.login import login_user, logout_user


user_session = Module(__name__)


@user_session.route('/session', methods=['POST'])
def login():
    """Handle user login form
    """
    user = User.query.filter_by(email=request.form['email']).first()
    valid = False
    message = "Invalid e-mail/password combination, please try again."
    if user:
        # Check that user is active
        if user.level < 1:
            message = "Please check your e-mail and click the \
                       verification link before logging in"
        else:
            # Check hash
            if not check_password_hash(user.pwhash, request.form['pass']):
                user = False
            else:
                remember = False
                valid = True
                if ('remember' in request.form.keys()
                        and request.form['remember'] == 'on'):
                        remember = True
                login_user(user, remember=remember)
    if not valid:
        flash(message)
    elif 'next' in request.form.keys():
        return redirect(request.form['next'])
    return redirect(url_for('default.index'))


@user_session.route('/session/out/', methods=['GET'])
def logout():
    """Handle user logout
    """
    logout_user()
    return redirect(url_for('default.index'))
