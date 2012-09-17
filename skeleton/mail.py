# -*- coding: utf-8 -*-
"""
    skeleton.mail
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Mail setup and related functionality with Flask-Mail

    :copyright: (c) 2012 by Jeff Long
"""
from . import app
from flask import render_template
from flask.ext.mail import Mail, Message
import os.path


mail = Mail(app)


def send(template, subject, recipients, **templatevars):
    """Send an e-mail with a jinja2 template"""
    path = os.path.dirname(__file__)
    plaintext_template = '%s%stemplates/emails/%s.txt' % (path, os.path.sep,
                                                          template)
    html_template = '%s%stemplates/emails/%s.html' % (path, os.path.sep,
                                                      template)
    msg = Message(subject,
                  sender=app.config['MAIL_DEFAULT_SENDER'],
                  recipients=recipients)

    # Plain-text template
    if os.path.exists(plaintext_template):
        msg.body = render_template('emails/%s.txt' % template,
                                   **templatevars).encode('ascii', 'ignore')
    else:
        app.logger.debug('Plain-text e-mail template does not exist for "%s"'
                         % plaintext_template)

    # HTML template
    if os.path.exists(html_template):
        msg.html = render_template('emails/%s.html' % template,
                                   **templatevars).encode('ascii', 'ignore')
    else:
        app.logger.debug('HTML e-mail template does not exist for "%s"'
                         % html_template)

    """This is only here temporarily until I can figure out why setting
    CSRF_ENABLED in TestingConfig seems to make Flask-Mail ignore the TESTING
    flag and send mail anyways. It's annoying to have a #pragma: no cover tag,
    it feels like wearing the python cone of shame :(."""
    if app.config['TESTING']:
        return True
    return mail.send(msg)  # pragma: no cover
