import random
from fabric.contrib.files import append, exists
from fabric.api import cd, env, local, run 

REPO_URL = 'https://github.com/yueda27/py-tdd.git'
env.key_filename='~/.ssh/yueda_key_pair.pem'

def deploy():
    try:
        site_folder = '/home/ec2-user/pytdd'
        run(f'mkdir -p {site_folder}')
        with cd(site_folder):
            _get_latest_source()
        with cd(f'{site_folder}/py-tdd'):
            _create_or_update_venv()
            _update_dotenv()
            _update_static_files()
            _update_database()
    except:
        # with cd('/home/ec2-user'):
        #     run("rm -rf pytdd")
        pass

def _get_latest_source():
    if exists('py-tdd/.git'):
        with cd('py-tdd'):
            run('git fetch')
            return
    else:
        run(f'git clone {REPO_URL}')
    #current_commit = local('git log -n 1 --format=%H', capture=True)
    #run(f'git reset --hard {current_commit}')

def _update_dotenv():
    run("pipenv install")

def _create_or_update_venv():
    append('.env', "DJANGO_DEBUG_FALSE=y")
    current_contents = run("cat .env")
    if 'DJANGO_SECRET_KEY' not in current_contents:
        new_secret = "".join(random.SystemRandom().choices('abcdefghijklmnopqrstuvwxyz123456789', k=50))
    append(".env", f'DJANGO_SECRET_KEY={new_secret}')

def _update_static_files():
    run('pipenv run python manage.py collectstatic --noinput')

def _update_database():
    run('pipenv run python manage.py migrate --noinput')