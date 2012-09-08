flask-skeleton
==============

A basic Flask project skeleton that includes a user system with generic functions such as account recovery, remember me, and e-mail verification.

Getting Started
--
I'd recommend getting started with a new virtualenv and installing the required modules in `requirements.txt`. If you've got virtualenv wrapper, that's:

    mkvirtualenv flaskskeleton
    pip install -r requirements.txt

Then open up `skeleton/config.py` in your favorite editor and change the essentials (database URIs, most importantly). Once that's set, create your tables either manually or by running `python create_tables.py`.

If everything went smooth, you should be able to run `python runserver.py` and visit http://127.0.0.1:5000 in your browser to see the basics. Note that e-mail may or may not work with your setup, but if it doesn't, you can use gmail (pretty straight-forward in `config.py`).

I've included a basic `Makefile` for simple tasks as well. `make tests` will run nosetests with coverage, `make pep8` will run pep8 (I've got some cleaning up to do here), and `make clean` will remove your `.pyc` files.

Questions/comments
--
This is my first stab at a generic Flask skeleton. It's also my first attempt to test with 100% coverage. That said, any and all feedback (especially corrections on best practices, etc) is more than welcome.

