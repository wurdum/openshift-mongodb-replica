import os
import logging
import logging.handlers
import commands
import env


class GmailSMTPHandler(logging.handlers.SMTPHandler):
    def emit(self, record):
        try:
            import smtplib
            from email.mime.text import MIMEText

            content = MIMEText(record.msg)
            content['From'] = self.fromaddr
            content['To'] = ', '.join(self.toaddrs)
            content['Subject'] = '%s in "%s" line %d' % (self.getSubject(record), record.filename, record.lineno)

            server = smtplib.SMTP(self.mailhost)
            server.starttls()
            server.login(self.username, self.password)
            server.sendmail(self.fromaddr, self.toaddrs, content.as_string())
            server.quit()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)


class OpenShiftLogger(logging.FileHandler):
    def __init__(self, filename, mode):
        filename = os.path.join(env.LOG_DIR, filename)
        logging.FileHandler.__init__(self, filename, mode=mode)


class DummyMutex:
    def __init__(self, filename):
        self.filename = filename
        self.fd = None
        self.pid = os.getpid()

    def acquire(self):
        try:
            self.fd = os.open(self.filename, os.O_CREAT | os.O_EXCL | os.O_RDWR)
            os.write(self.fd, "%d" % self.pid)
            return 1
        except OSError:
            self.fd = None
            return 0

    def release(self):
        if not self.fd:
            return 0
        try:
            os.close(self.fd)
            os.remove(self.filename)
            self.fd = None
            return 1
        except OSError:
            return 0

    def __del__(self):
        self.release()


class ArgumentsParser(object):
    def __init__(self, args):
        if len(args) == 1 or args[1] not in commands.get_commands().values():
            raise SyntaxError('control command was not specified')

        self._command = args[1]
        self._caller = 'from %s' % args[2] if len(args) >= 3 else self._command

    @property
    def command(self):
        return self._command

    @property
    def caller(self):
        return self._caller
