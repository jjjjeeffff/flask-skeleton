from flask import session, redirect, url_for, request
from functools import wraps
import time


# Create require_login decorator
def require_login(fn):
    @wraps(fn)
    def validate(*args, **kwargs):
        if not session.get('user'):
            return redirect(url_for('session.login', next=request.url))
        return fn(*args, **kwargs)
    return validate


def datetime_to_relative(input):
    fudge = 1
    delta = long(time.time()) - long(time.mktime(input.timetuple()))

    if delta < (1 * fudge):
        return 'about a second ago'
    elif delta < (60 * (1 / fudge)):
        return 'about %d seconds ago' % (delta)
    elif delta < (60 * fudge):
        return 'about a minute ago'
    elif delta < (60 * 60 * (1 / fudge)):
        return 'about %d minutes ago' % (delta / 60)
    elif delta < (60 * 60 * fudge) or delta / (60 * 60) == 1:
        return 'about an hour ago'
    elif delta < (60 * 60 * 24 * (1 / fudge)):
        return 'about %d hours ago' % (delta / (60 * 60))
    elif delta < (60 * 60 * 24 * fudge) or delta / (60 * 60 * 24) == 1:
        return 'about a day ago'
    else:
        return 'about %d days ago' % (delta / (60 * 60 * 24))
