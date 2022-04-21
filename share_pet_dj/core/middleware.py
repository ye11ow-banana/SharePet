# import logging
# logger = logging.Logger(__name__)

from core.pages import handler500


class Process500:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        response = self._get_response(request)
        return response

    @staticmethod
    def process_exception(request, exception):
        # logger.error(f'url: {request.path}, error: {exception}')

        return handler500(request, error=exception)
