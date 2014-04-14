# -*- coding: utf-8 -*-
"""
    skeleton.forms.signup
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    User registration form definition with helpers.

    :copyright: (c) 2012 by Jeff Long
"""
from wtforms import Form, TextField, BooleanField, \
    PasswordField, validators, ValidationError
from ..models.user import User


def signup_email_check(form, field):
    """Checks to see if a user with the requested e-mail address already
    exists and raises a ValidationError if it does.
    """
    users = User.query.filter_by(email=field.data).count()
    if users > 0:
        raise ValidationError('A user with this e-mail already exists.')


class SignupForm(Form):
    """Definition for the registration form """
    new_email = TextField('Email Address', [
        validators.Length(min=6, max=120),
        validators.Required(),
        validators.Email(message='Invalid e-mail address.'),
        signup_email_check])
    password = PasswordField('Password', [
        validators.Length(min=6, max=20),
        validators.Required(),
        validators.EqualTo('password_confirm', message='Passwords must match')
    ])
    password_confirm = PasswordField('Confirm Password', [
        validators.Length(min=6, max=20),
        validators.Required()])
    agree = BooleanField('I accept the TOS', [validators.Required()])
