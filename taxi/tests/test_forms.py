from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTests(TestCase):
    def test_driver_creation_form_with_additional_fields(self):
        form_data = {
            "username": "test123",
            "password1": "user232342",
            "password2": "user232342",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "AAA33333",
        }
        form = DriverCreationForm(data=form_data)
        print(form.errors)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
