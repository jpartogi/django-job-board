# $Id: setup.py 367a51c79b19 2009/08/22 13:58:55 jpartogi $
#!/usr/bin/env python

from distutils.core import setup

app_name = 'job_board'

setup(  
    name='django-job-board',
    version='0.9.0',
    packages=[app_name, '%s.templatetags' % app_name],
    package_data = {app_name: ['templates/%s/*.html' % app_name]},
    author = 'Joshua Partogi',
    author_email = 'joshua.partogi@gmail.com',
    url = 'http://github.com/scrum8/django-job-board',
    download_url = 'http://github.com/scrum8/django-job-board/downloads',

    license = "BSD License",
    keywords = "django job board",
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    platforms = ['any'],
)
