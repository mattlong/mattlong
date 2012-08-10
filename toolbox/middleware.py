import logging

class LogUnhandledExceptions(object):
    def process_exception(self, request, exception):
        logging.exception(request.build_absolute_uri())
