from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random

REPO_URL = 'https://github.com/andreitch/superlists.git'


def deploy():
    site_folder = f'/home/{env.user}/sites/{env.host}'
    source_folder = site_folder + '/source'
    _get_latest_source(site_folder)
    _create_directory_structure_if_necessary(site_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(site_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)


def restart():
    run(f'service gunicorn-{env.host} restart')


def _create_directory_structure_if_necessary(site_folder):
    for subfolder in ('database', 'static', 'virtualenv', 'source'):
        run(f'mkdir -p {site_folder}/{subfolder}')


def _get_latest_source(site_folder):
    run(f'mkdir -p {site_folder}')
    if exists(site_folder + '/.git'):
        run(f'cd {site_folder} && git fetch')
    else:
        run(f'git clone {REPO_URL} {site_folder}')
        current_commit = local("git log -n 1 --format=%H", capture=True)
        run(f'cd {site_folder} && git reset --hard {current_commit}')


def _update_settings(source_folder, site_name):
    settings_path = source_folder + '/superlists/settings.py'
    sed(settings_path, "DEBUG = True", "DEBUG = False")
    sed(settings_path,
        'ALLOWED_HOSTS =.+$',
        f'ALLOWED_HOSTS = ["{site_name}"]'
        )
    secret_key_file = source_folder + '/superlists/secret_key.py'
    if not exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, f'SECRET_KEY = "{key}"')
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')


def _update_virtualenv(site_folder):
    virtualenv_folder = site_folder + '/virtualenv'
    if not exists(virtualenv_folder + '/bin/pip'):
        run(f'python3.7 -m venv {virtualenv_folder}')
    run(f'{virtualenv_folder}/bin/pip install -r {site_folder}/requirements.txt')


def _update_static_files(source_folder):
    run(
        f'cd {source_folder}'
        ' && ../virtualenv/bin/python manage.py collectstatic --noinput'
    )


def _update_database(source_folder):
    run(
        f'cd {source_folder}'
        ' && ../virtualenv/bin/python manage.py migrate --noinput'
    )
