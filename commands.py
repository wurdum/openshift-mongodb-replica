class BaseCommand(object):
    def __init__(self, processes, logger):
        if processes is None or logger is None:
            raise ValueError('some of the arguments are empty')

        if not isinstance(processes, list):
            processes = [processes]

        self._processes = processes
        self._logger = logger


class StartCommand(BaseCommand):
    def do(self, instance_name):
        for process in self._processes:
            process.start()
            self._logger.info('[%s] started %s' % (instance_name, process))


class StopCommand(BaseCommand):
    def do(self, instance_name):
        for subject in self._processes:
            subject.stop()
            self._logger.info('[%s] stopped %s' % (instance_name, subject))


class StartStoppedCommand(BaseCommand):
    def do(self, instance_name):
        for process in self._processes:
            if not process.is_started:
                process.start()
                self._logger.info('[%s] started %s' % (instance_name, process))


class TryStartCommand(BaseCommand):
    def do(self, instance_name):
        for process in self._processes:
            result = process.try_start()

            msg = ''
            if result[0] == 0:
                msg = '[%s] started %s' % (instance_name, process)
            elif result[0] == 1:
                msg = '[%s] can\'t start, already running %s' % (instance_name, process)
            elif result[0] == -1:
                msg = '[%s] error during start %s: %s' % (instance_name, process, result[1])

            self._logger.critical(msg)


class TryStopCommand(BaseCommand):
    def do(self, instance_name):
        for process in self._processes:
            result = process.try_stop()

            msg = ''
            if result[0] == 0:
                msg = '[%s] stopped %s' % (instance_name, process)
            elif result[0] == 1:
                msg = '[%s] can\'t stop, already stopped %s' % (instance_name, process)
            elif result[0] == -1:
                msg = '[%s] error during stop %s: %s' % (instance_name, process, result[1])

            self._logger.critical(msg)


ALL_COMMANDS = type('Enum', (), {
    'START': 'start',
    'STOP': 'stop',
    'START_STOPPED': 'start_stopped',
    'TRY_START': 'try_start',
    'TRY_STOP': 'try_stop'
})


def get_commands():
    return dict([(key, value) for key, value in ALL_COMMANDS.__dict__.items() if not key.startswith('__')])


def get_command_handler(command):
    if command == ALL_COMMANDS.START:
        return StartCommand

    elif command == ALL_COMMANDS.STOP:
        return StopCommand

    elif command == ALL_COMMANDS.START_STOPPED:
        return StartStoppedCommand

    elif command == ALL_COMMANDS.TRY_START:
        return TryStartCommand

    elif command == ALL_COMMANDS.TRY_STOP:
        return TryStopCommand

    raise ValueError('unknown command encountered - "%s"' % command)