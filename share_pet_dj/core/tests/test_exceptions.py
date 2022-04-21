from django.test import SimpleTestCase

from core.exceptions import CreateInstanceError


class CreateInstanceErrorTest(SimpleTestCase):
    def test_inheritance(self):
        self.assertTrue(isinstance(CreateInstanceError(''), Exception))

    def test_error_message(self):
        error = CreateInstanceError('ClassName')
        self.assertEquals(
            str(error), 'Instance of the class `ClassName` cannot be created.')
