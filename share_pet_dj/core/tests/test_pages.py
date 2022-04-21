from django.http import HttpRequest
from django.test import SimpleTestCase

from core.pages import handler500, handler404, handler400


class Handler500ViewTest(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        request = HttpRequest()
        request.method = 'GET'
        cls.response = handler500(request)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_template(self):
        self.assertEquals(self.response.template_name[0], 'core/500.html')


class Handler404ViewTest(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        request = HttpRequest()
        request.method = 'GET'
        cls.response = handler404(request)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_template(self):
        self.assertEquals(self.response.template_name[0], 'core/404.html')


class Handler400ViewTest(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        request = HttpRequest()
        request.method = 'GET'
        cls.response = handler400(request)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_template(self):
        self.assertEquals(self.response.template_name[0], 'core/400.html')
