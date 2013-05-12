import os
import env


def create_if_not_exists(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)


LOCK_FILE_NAME = 'processes.lock'
LOCK_FILE = os.path.join(env.TMP_DIR, LOCK_FILE_NAME)

SSH_STATIC_DIR = os.path.join(env.DATA_DIR, 'ssh')
SSH_KEY = os.path.join(env.REPO_DIR, 'ssh/id_rsa')
SSH_KNOWN_HOSTS = os.path.join(SSH_STATIC_DIR, 'known_hosts')
SSH_COMMAND_PREFIX = 'ssh -i ' + SSH_KEY + ' -o StrictHostKeyChecking=no -o UserKnownHostsFile=' + SSH_KNOWN_HOSTS

SCRIPTS_DIR = os.path.join(env.REPO_DIR, 'scripts')
MONGO_CONFIG_SCRIPT = os.path.join(SCRIPTS_DIR, 'replace.sh')
MONGO_ROOT_DIR = os.path.join(env.DATA_DIR, 'mongo')
MONGO_DATA_DIR = os.path.join(MONGO_ROOT_DIR, 'data')
MONGO_PID_DIR = os.path.join(MONGO_ROOT_DIR, 'pid')
MONGO_CONFIG = os.path.join(MONGO_ROOT_DIR, 'mongodb.conf')

create_if_not_exists(SSH_STATIC_DIR)
create_if_not_exists(MONGO_DATA_DIR)
create_if_not_exists(MONGO_PID_DIR)

CREDENTIALS = [
    {'name':'m1', 'uuid':'###', 'port':'30001'},
    {'name':'m2', 'uuid':'###', 'port':'30002'},
    {'name':'m3', 'uuid':'###', 'port':'30003'}
]