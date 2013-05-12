import os
from subprocess import Popen, PIPE
import signal
import time
import config
import replica


class BaseProcess(object):
    _name = None

    def __init__(self, instance):
        if instance is None or not isinstance(instance, replica.Instance):
            raise SyntaxError('expected non-empty instance value')

        self._instance = instance

    @property
    def pid(self):
        lsof = 'lsof -i tcp:' + self._instance.port
        awk = ['awk', '{print $2}']
        lsof_out = Popen(lsof.split(), stdout=PIPE)
        awk_out = Popen(awk, stdin=lsof_out.stdout, stdout=PIPE)
        out = awk_out.communicate()[0]

        return int(out.split('\n')[1]) if out else None

    @property
    def is_started(self):
        return self.pid is not None

    def start(self):
        raise RuntimeError('not implemented')

    def stop(self):
        pid = self.pid
        if pid is None:
            raise RuntimeError('Can\'t stop already stopped %s' % self._name)

        os.kill(pid, signal.SIGTERM)
        try:
            time.sleep(0.5)
            os.kill(pid, 0)
            raise Exception('Can\'t kill %s process' % self._name)
        except OSError:
            pass

    def try_start(self):
        return (1, None) if self.is_started else self._run_safe(self.start)

    def try_stop(self):
        return (1, None) if not self.is_started else self._run_safe(self.stop)

    def _run_safe(self, func):
        try:
            func()
        except Exception as ex:
            return -1, ex
        else:
            return 0, None

    def __repr__(self):
        return self._instance


class Tunnel(BaseProcess):
    _name = 'tunnel'

    def start(self):
        if self.is_started:
            raise RuntimeError('Tunnel already started')

        command = config.SSH_COMMAND_PREFIX + ' -f -N -L ' + \
                  ':'.join([replica.REPLICA.local.ip, self._instance.port, self._instance.ip, self._instance.port]) + \
                  ' ' + self._instance.ssh

        Popen(command.split()).wait()

    def __repr__(self):
        return 'tunnel %s' % super(Tunnel, self).__repr__()


class Mongo(BaseProcess):
    _name = 'mongo instance'

    def start(self):
        if self.is_started:
            raise RuntimeError('Mongo instance already run,')

        self._recreate_config_file()
        self._run_mongod()

    def _recreate_config_file(self):
        command = 'sh %s' % config.MONGO_CONFIG_SCRIPT
        Popen(command.split()).wait()

    def _run_mongod(self):
        command = 'mongod --config %s' % config.MONGO_CONFIG
        Popen(command.split()).wait()

    def __repr__(self):
        return 'mongo %s' % super(Mongo, self).__repr__()
