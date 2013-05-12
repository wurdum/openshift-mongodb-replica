import os
import sys
import time
import logging
import logging.config


execution_path = os.environ.get('OPENSHIFT_REPO_DIR', '')
if execution_path:
    sys.path.append(execution_path)

logging.config.fileConfig(os.path.join(execution_path, 'log.conf'))
logger = logging.getLogger('main')

try:
    import config
    import commands
    import extensions
    from replica import REPLICA
    from processes import Tunnel, Mongo

    os.environ['MONGO_INSTANCE_PORT'] = REPLICA.local.port
except ImportError as ex:
    logger.exception('can\'t import modules: %s' % ex)
    sys.exit(1)

VERSION = '0.0.19'
INSTANCE = REPLICA.local.name


def run_safe(process, commandHandler):
    try:
        commandHandler(process, logger).do(INSTANCE)

    except Exception as ex:
        logger.exception('[%s] (%s) %s' % (INSTANCE, process, ex))


def main(args):
    lock = extensions.DummyMutex(config.LOCK_FILE)
    sibling = REPLICA.get_sibling()
    while True:
        if lock.acquire():
            logger.info('[%s] lock acquired %s' % (INSTANCE, args.caller))
            logger.info('[%s] running "%s for [%s] %s' % (INSTANCE, args.command, sibling, args.caller))

            commandHandler = commands.get_command_handler(args.command)

            for instance in sibling:
                run_safe(Tunnel(instance), commandHandler)

            run_safe(Mongo(REPLICA.local), commandHandler)

            lock.release()
            logger.info('[%s] lock released %s' % (INSTANCE, args.caller))

            sys.exit(1)
        else:
            logger.info('[%s] waiting for lock %s' % (INSTANCE, args.caller))
            time.sleep(0.3)


if __name__ == '__main__':

    args = None
    try:
        args = extensions.ArgumentsParser(sys.argv)
    except SyntaxError as ex:
        logger.exception('[%s] %s' % (INSTANCE, ex))
        sys.exit(1)

    main(args)