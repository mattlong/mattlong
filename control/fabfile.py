#!/usr/bin/env python
import os
from fabric.api import *

# http://www.abidibo.net/blog/2012/06/29/deploy-django-applications-nginx-uwsgi-virtualenv-south-git-and-fabric-part-5//

env.hosts = ['127.0.0.1']
env.user = 'ubuntu'
env.key_filename = os.environ.get('MATTLONG_KEY')

env.settings = 'production'
env.path = os.environ.get('MATTLONG_PATH')
env.release = 'latest'

def setup():
    run('mkdir -p %(path)s' % env)
    with cd(env.path):
        run('virtualenv --no-site-packages .')
        run('git clone git://github.com/mattlong/mattlong.git mattlong')

def deploy():
    with cd(env.path):
        sha1 = None
        with cd('mattlong'):
            run('git fetch origin')
            run('git reset --hard origin/master')
            sha1 = run('git rev-parse HEAD').stdout
        run('echo "%s" >> releases' % (sha1,))
        run('./bin/pip install -r mattlong/requirements.txt')
        #TODO: copy in correct settings/local.py
        #TODO: restart uwsgi
