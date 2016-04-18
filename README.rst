Knowledge Base
==============

Django project to manage Scientific Knowledge Bases.


Installation intructions
========================

Dependencies
------------
* python 2.7 (or higher)
* pip
* Django 
* bibtexparser
* django-contrib-comments
* django-tagging
* pytz
* tagging

Installation
------------

Instructions::

  git clone https://github.com/dguarino/kb.git
  cd kb
  

Virtual env
___________

We recommend to install kb using the virtualenv python environment manager (http://pypi.python.org/pypi/virtualenv/), to prevent potential
conflicts with standard versions of required libraries. Users can follow for example http://simononsoftware.com/virtualenv-tutorial tutorial or just do the following steps:
 
 * Install virtualenv
 * Create (for example in your home directory) a directory where all virtual environments will be created home/virt_env
 * Create the virtual environment for kb:: 
    
    virtualenv virt_env/kb/ --verbose --no-site-packages

 * Load the virtual environment for kb by::
 
    source virt_env/kb/bin/activate

If you have virtualenv-wrapper installed it is even simpler. Just type::

	$ mkvirtualenv kb
	New python executable in kb/bin/python
	Installing Setuptools............done.
	Installing Pip...................done.

Your shell should look now something like::

	(kb) Username@Machinename:~$

You can now install all the requirements using pip::

	(kb) $ pip install -r requirements.txt

You can use pip to view the installed packages::

	(kb) $ pip freeze

Once installed, you shoud create the demo-server with::

	(kb) $ python manage.py makemigrations maps
	(kb) $ python manage.py migrate

Then you should create an admin for the website::

	(kb) $ python manage.py createsuperuser
	Username: ...
	Email address: ...
	Password: ...
	Password (again): ...
	Superuser created successfully

And now you can run the server::
	(kb) $ python manage.py runserver

To access the interface, open a browser and hit the address:: 

	http://127.0.0.1:8000/knowledgebase

Ant to access the admin (in order to create new users and so on), hit the address::

	http://127.0.0.1:8000/knowledgebase/admin
