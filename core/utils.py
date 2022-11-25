import traceback

from rest_framework.views import exception_handler


def debug_exception_handler(exc, context):
    print('\n--- REST EXCEPTION ---\n')
    traceback.print_exc()
    print()
    return exception_handler(exc, context)
