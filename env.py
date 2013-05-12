import os


NAME = os.environ.get('OPENSHIFT_APP_NAME', 'm1')
TMP_DIR = os.environ.get('OPENSHIFT_TMP_DIR', '/tmp')
LOG_DIR = os.environ.get('OPENSHIFT_DIY_LOG_DIR', '/tmp')
DATA_DIR = os.environ.get('OPENSHIFT_DATA_DIR', '/tmp')
REPO_DIR = os.environ.get('OPENSHIFT_REPO_DIR', '/srv/mongo-replica-config')
LOCAL_IP = os.environ.get('OPENSHIFT_INTERNAL_IP', '127.0.0.1')