# -*- coding: utf-8 -*-
"""
    skeleton.views.default
    ~~~~~~~~~~~~~~~~~~~~~~

    Landing page views. Where accounts are created and users login
    and dreams are made.

    :copyright: (c) 2012 by Jeff Long
"""


from flask import Module, request, render_template, session
from flask.ext.login import current_user
from ..forms.signup import SignupForm


default = Module(__name__)


@default.route('/')
def index():
    """This is the landing page, which will display a login form and a
    registration form.
    """
    if current_user.is_authenticated():
        return render_template('index/authed.html')
    else:
        form = SignupForm(session.get('form'))
        if session.get('form'):
            # Re-validate form here to determine errors to display
            form.validate()
            session.pop('form', None)
        return render_template('index/index.html', form=form,
                               next=request.args.get('next'))
