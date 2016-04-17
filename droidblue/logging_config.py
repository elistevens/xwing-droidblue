"""
# logging
import logging
log = logging.getLogger(__name__)
"""
# === NOTE ===
# This file cannot import any 3rd-party libraries, since mms.logging_config must
# be imported by app.wsgi before the virtual env is set up (and hence any
# 3rd-party libs won't be available yet).  Python stdlib and mms are both okay.
#
# This is also true for anything imported from this file (obviously).

# stdlib
import logging
import logging.handlers
# import platform

# class PlatformIndependentSysLogHandler(logging.handlers.SysLogHandler):
#     '''Handler for writing to syslog across platforms.'''
#     def __init__(self, *args, **kwargs):
#         system = platform.system()
#         if system == 'Linux':
#             syslogSocket = '/dev/log'
#         elif system == 'Darwin':
#             syslogSocket = '/var/run/syslog'
#         elif system == 'Windows':
#             syslogSocket = ('localhost', 514)
#         else:
#             raise ValueError('Unsupported platform: {}'.format(system))
#
#         super(PlatformIndependentSysLogHandler, self).__init__(address=syslogSocket, *args, **kwargs)
#
#         # syslog only logs the message by default
#         self.setFormatter(logging.Formatter(fmt="%(asctime)s %(levelname)-8s pid:%(process)d,%(thread)d %(name)s:%(lineno)03d:%(funcName)s %(message)s"))
#
# class DynamicFileSysLogHandler(PlatformIndependentSysLogHandler):
#     '''
#         Syslog handler that writes to a specified logfile.
#
#         local4 is configured to use a dynamic log file, as determined by the
#         ``programname`` property (which is the leading tag, i.e. ``"tag: message"``).
#
#         This handler automatically sets the tag in the formatter.
#
#         Usage::
#
#             logger = logging.getLogger(__name__)
#             logger.addHandler(DynamicFileSysLogHandler('foobar'))
#     '''
#     def __init__(self, name, *args, **kwargs):
#         '''
#             :param name: Name to use in log file, e.g. ``name=foo`` -> ``/var/log/mms/foo.log``
#             :type name: string
#         '''
#         super(DynamicFileSysLogHandler, self).__init__(facility=logging.handlers.SysLogHandler.LOG_LOCAL4)
#         self.name = name.replace('/', '_') # no shenanigans!
#
#         # Some formatting has already been set in syslog config
#         self.setFormatter(logging.Formatter(fmt="{}: %(levelname)-8s pid:%(process)d,%(thread)d %(name)s:%(lineno)03d:%(funcName)s %(message)s".format(self.name)))
#
# class ErrorLog(object):
#     def __init__(self):
#         '''
#             Creates a limited logging object that only logs exceptions to
#             the syslog using the local7 facility.
#         '''
#         self._log = logging.getLogger(__name__)
#         self._log.setLevel(logging.ERROR)
#
#         self._log.addHandler(PlatformIndependentSysLogHandler(facility=logging.handlers.SysLogHandler.LOG_LOCAL7))
#
#     def exception(self):
#         '''
#             Only exceptions may be logged.  No message may be given; this is to
#             ensure that no patient data makes it to the exception log.
#             Only stacktrace information should be sent.
#         '''
#         self._log.exception('Exception:')
#
#     def __getattr__(self, attr):
#         raise AttributeError('Only exceptions may be logged with this error logger')

# error_log = ErrorLog()

formatter = logging.Formatter("%(asctime)s %(levelname)-8s pid:%(process)d,%(thread)d %(name)s:%(lineno)03d:%(funcName)s %(message)s")

streamHandler = logging.StreamHandler()
streamHandler.setLevel(logging.DEBUG)
streamHandler.setFormatter(formatter)

root_logger = logging.getLogger()
root_logger.setLevel(logging.WARN)
root_logger.addHandler(streamHandler)

# # 3rd party packages
# logging.getLogger('pydicom').setLevel(logging.WARN)
# logging.getLogger('OpenGL').setLevel(logging.WARN)
#
# # in-house
# logging.getLogger('couchable').setLevel(logging.INFO)

logging.getLogger(__name__).info("Logging configured.")

# eof
