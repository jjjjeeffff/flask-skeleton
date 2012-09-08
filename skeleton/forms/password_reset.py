# -*- coding: utf-8 -*-
"""
    skeleton.forms.password_reset
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Password reset form

    :copyright: (c) 2012 by Jeff Long
"""


from flask.ext.wtf import Form, Required, PasswordField, validators


class PasswordResetForm(Form):
    """Definition for the password reset form """
    password = PasswordField('Password', [
        validators.Length(min=6, max=20),
        Required(),
        validators.EqualTo('password_confirm', message='Passwords must match')
    ])
    password_confirm = PasswordField('Confirm Password', [
        validators.Length(min=6, max=20),
        Required()])
