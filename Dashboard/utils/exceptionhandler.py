def custom_exception_handler(exc, content):
    handler = {
        'ValidationError': _handle_generic_error,
        'Http404': _handle_generic_error,
        'PermissionDenied': _handle_generic_error,
        'NotAuthenticated': _handle_generic_error
    }


def _handle_generic_error(exc, content, response):
    return response
