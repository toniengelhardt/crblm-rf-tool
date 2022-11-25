import logging

from django.conf import settings


class RequireTestingFalse(logging.Filter):
    def filter(self, record):
        return not settings.TEST
