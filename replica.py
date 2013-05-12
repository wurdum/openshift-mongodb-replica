from subprocess import Popen, PIPE
import config
import env


class Replica(object):
    def __init__(self, instances):
        if len(instances) != 3:
            raise ValueError('replica should consists of 3 instances')

        self._instances = instances
        self._local = [inst for inst in self._instances if inst.name == env.NAME][0]

    @property
    def local(self):
        return self._local

    def get_all(self):
        return self._instances

    def get_sibling(self):
        return [inst for inst in self._instances if inst.name != env.NAME]


class Instance(object):
    _ip = None

    def __init__(self, name, uuid, port):
        if not name or not uuid:
            raise ValueError('some of the arguments is empty')

        self._uuid = uuid
        self._name = name
        self._port = port

    @property
    def name(self):
        return self._name

    @property
    def uri(self):
        return self._name + '-saber.rhcloud.com'

    @property
    def ssh(self):
        return '%s@%s' % (self._uuid, self.uri)

    @property
    def port(self):
        return self._port

    @property
    def ip(self):
        if self._ip is not None:
            return self._ip

        if env.NAME == self._name:
            self._ip = env.LOCAL_IP
            return self._ip

        command = config.SSH_COMMAND_PREFIX.split()
        command = command + [self.ssh, 'echo $OPENSHIFT_INTERNAL_IP']

        command_out = Popen(command, stdout=PIPE)
        self._ip = command_out.communicate()[0].strip()
        return self._ip

    def __repr__(self):
        return '[%s - ip:%s, port:%s]' % (self.uri, self.ip, self.port)

INSTANCES = [Instance(inst['name'], inst['uuid'], inst['port']) for inst in config.CREDENTIALS]
REPLICA = Replica(INSTANCES)