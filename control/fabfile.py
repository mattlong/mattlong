#!/usr/bin/env python
import os
from fabric.api import *

# http://www.abidibo.net/blog/2012/06/29/deploy-django-applications-nginx-uwsgi-virtualenv-south-git-and-fabric-part-5//

env.hosts = ['127.0.0.1']
env.user = 'ubuntu'
env.key_filename = os.environ['MATTLONG_KEY']

env.settings = 'production'
env.path = os.environ['MATTLONG_PATH']
env.static_path = os.environ['MATTLONG_ORG_STATIC_PATH']
env.vassal_dir = os.environ['UWSGI_VASSAL_DIR']
env.release = 'latest'

def setup():
    run('mkdir -p %(path)s' % env)
    sudo('rm -rf %(path)s/*' % env)
    run('mkdir -p %(static_path)s' % env)
    sudo('mkdir -p /etc/mattlong.org/')
    sudo('chown ubuntu:ubuntu /etc/mattlong.org/')

    with cd(env.path):
        run('virtualenv --no-site-packages .')
        #run('git clone git://github.com/mattlong/mattlong.git mattlong')
        run('cp -r /home/ubuntu/repos/mattlong ./mattlong')
        run('./bin/pip install -r ./mattlong/requirements.txt')
        #run('ln -s ~/.mattlong/defaultdb mattlong/mattlongweb/')

def deploy(use_git='false'):
    use_git = use_git.lower() == 'true'

    env_var_str = 'export'
    env_vars = {}
    for key, value in os.environ.items():
        if key.find('MATTLONG') == 0:
            env_var_str += ' %s=\'%s\'' % (key,value)
            env_vars['key'] = value

    with cd(env.path):
        sha1 = None

        with cd('mattlong'):

            if use_git:
                run('git fetch origin')
                run('git reset --hard HEAD')
                sha1 = run('git rev-parse HEAD').stdout
            else:
                run('rsync -a --delete /home/ubuntu/repos/mattlong/ ./')
                run('find . -name "*.pyc" | xargs rm')
                run('find . -name ".git" | xargs rm -rf')


            with prefix(env_var_str):
                run('python manage.py collectstatic --noinput')

        if use_git and sha1:
            run('echo "%s" >> releases' % (sha1,))

        run('./bin/pip install -r mattlong/requirements.txt')
        run('cat /etc/mattlong.org/uwsgi-envvars >> mattlong/mattlongweb/mattlong.ini')

        sudo('cp mattlong/mattlongweb/mattlong.ini %s/' % (env.vassal_dir,))
