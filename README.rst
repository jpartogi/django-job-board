django-job-board
================

django-job-board is a dead simple django based pluggable job board application
that is extracted from the original Scrum8.com and is currently online at http://jobs.scrum8.com

Dependencies
------------
To install django-job-board on your django site, you need these two django applications:

#. django-tagging: http://code.google.com/p/django-tagging/
#. django-commons: http://github.com/scrum8/django-commons/

Installation
------------
To install django-job-board on your django site, you would need to do the following steps:
#. Add django-job-board to your django project INSTALLED_APPS settings as such:
::

INSTALLED_APPS = (
    ...
    'job_board',
    'commons',
    'tagging',
)

If you already have django-commons and django-tagging installed, then you don't need to
add it again on the INSTALLED_APPS configuration.

#. Add django-job-board to your url settings
If job board is the root url in your project then you need to add the following url
configuration to urls.py:
::

url(r'^', include('job_board.urls')),

If not then you may add it as such:
::

url(r'^jobs/$', include('job_board.urls')),

#. Synchronize the database with:

>>> python manage.py syncdb

#. Add the job categories from django admin

#. django-job-board should be available on your site now

Template customization
----------------------
You may customize and override django-job-board according to your needs.
In your django-project's TEMPLATE_DIRS you may add 'job_board' directory underneath it.
The templates that should exists is:

#. form.html        : This is the template for the add new job
#. base_form.html   : This is the actual form that is shared between form.html and preview.html
#. list.html        : This is the template for displaying the currently listed jobs
#. view.html        : This is the template for displaying the detail of the job
#. preview.html     : This is the template for previewing the data before it is submitted to the database
#. feed.html        : This is the template for displaying the job feeds. You may or may not override this template.