from django.http import HttpRequest
from django.test import SimpleTestCase

from core.middleware import Process500
from core.pages import Handler500View


class Process500Test(SimpleTestCase):
    def test_init(self):
        middleware = Process500('response')
        self.assertEquals(middleware._get_response, 'response')

    def test_call(self):
        response = Process500(lambda x: x + '|||')('request')

        self.assertEquals(response, 'request|||')

    def test_process_exception(self):
        middleware = Process500('')
        request = HttpRequest()
        request.method = 'GET'
        response = middleware.process_exception(request, 'Exception!')

        self.assertEquals(response.context_data['error'], 'Exception!')
        self.assertTrue(
            isinstance(response.context_data['view'], Handler500View))
