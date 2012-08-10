#!/usr/bin/env python
import os
from fabric.api import *

# http://www.abidibo.net/blog/2012/06/29/deploy-django-applications-nginx-uwsgi-virtualenv-south-git-and-fabric-part-5//

env.hosts = ['127.0.0.1']
env.user = 'ubuntu'
env.key_filename = os.environ.get('MATTLONG_KEY')

env.settings = 'production'
env.path = os.environ.get('MATTLONG_PATH')
env.static_path = os.environ.get('MATTLONG_STATIC_PATH')
env.vassal_dir = os.environ.get('UWSGI_VASSAL_DIR')
env.release = 'latest'

def setup():
    run('mkdir -p %(path)s' % env)
    sudo('rm -rf %(path)s/*' % env)
    run('mkdir -p %(static_path)s' % env)

    with cd(env.path):
        run('virtualenv --no-site-packages .')
        run('git clone git://github.com/mattlong/mattlong.git mattlong')
        run('./bin/pip install -r mattlong/requirements.txt')
        run('ln -s ~/.mattlong/defaultdb mattlong/mattlongweb/')

def deploy():
    with cd(env.path):
        sha1 = None
        with cd('mattlong'):
            run('git fetch origin')
            run('git reset --hard origin/master')
            sha1 = run('git rev-parse HEAD').stdout
            run('python manage.py collectstatic --noinput')

        run('echo "%s" >> releases' % (sha1,))
        run('./bin/pip install -r mattlong/requirements.txt')
        #TODO: copy in correct settings/local.py
        sudo('cp mattlong/mattlongweb/mattlong.ini %s/' % (env.vassal_dir,))
