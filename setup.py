#!/usr/bin/env python3
# encoding: utf-8

import os
from setuptools import setup, find_packages

def files(package, paths):
    skip = len(package)+1
    for path in paths:
        for dirpath, dirnames, filenames in os.walk(os.path.join(package, path)):
            for filename in filenames:
                yield os.path.join(dirpath, filename)[skip:]


setup(
    name         = 'rhw',
    version      = '0.1',
    description  = 'Red Hack Week Management Application',
    author       = 'Jakub Dorňák',
    author_email = 'jdornak@redhat.com',
    url          = 'https://github.com/misli/rhw',
    packages     = find_packages(),
    package_data = {
        'rhw': list(files('rhw', ['templates', 'static'])),
    },
    scripts      = ['bin/rhw-manage'],
    data_files   = [
        ('/etc/bash_completion.d', ['conf/bash_completion.d/rhw.bash']),
        ('/etc/httpd/conf.d', ['conf/httpd/rhw.conf']),
        ('/var/lib/rhw/data', []),
        ('/var/lib/rhw/htdocs', ['rhw/wsgi.py']),
        ('/var/lib/rhw/htdocs/static', []),
        ('/var/lib/rhw/htdocs/media', []),
    ],
)
