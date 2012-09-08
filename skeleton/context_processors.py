from . import app
from flask.ext.login import current_user


@app.context_processor
def inject_user():
    return dict(user=current_user)
