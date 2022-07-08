from django.contrib.auth import get_user_model
from django.test import TestCase

from django.urls import reverse

from taxi.models import Car, Manufacturer


CAR_URL = reverse("taxi:car-list")
MANUFACTURER_URL = reverse("taxi:manufacturer-list")
DRIVER_URL = reverse("taxi:driver-list")


class PublicListTests(TestCase):

    def test_car_list_login_required(self):
        res = self.client.get(CAR_URL)

        self.assertNotEqual(res.status_code, 200)

    def test_manufacturer_list_login_required(self):
        res = self.client.get(MANUFACTURER_URL)

        self.assertNotEqual(res.status_code, 200)

    def test_driver_list_login_required(self):
        res = self.client.get(DRIVER_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateListTests(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "2132432",
        )
        self.client.force_login(self.user)

    def test_retrieve_car_view(self):
        manufacturer = Manufacturer.objects.create(
            name="Audi",
            country="Germany"
        )
        Car.objects.create(
            model="A3",
            manufacturer=manufacturer
        )
        Car.objects.create(
            model="m6",
            manufacturer=manufacturer
        )

        res = self.client.get(CAR_URL)
        cars = Car.objects.all()

        self.assertEqual(
            list(res.context["car_list"]),
            list(cars)
        )

    def test_retrieve_manufacturer_view(self):
        Manufacturer.objects.create(
            name="RS6",
            country="Germany"
        )
        Manufacturer.objects.create(
            name="Camry",
            country="Japan"
        )

        res = self.client.get(MANUFACTURER_URL)

        manufacturers = Manufacturer.objects.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "123432432"
        )
        self.client.force_login(self.user)

    def test_create_driver(self):
        form_data = {
            "username": "test123",
            "password1": "user232342",
            "password2": "user232342",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "AAA33333",
        }
        self.client.post(reverse("taxi:create-driver"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])\
