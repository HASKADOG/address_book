from datetime import datetime
from unittest.mock import patch

import pytz
from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import Address, User


def mocked_requests(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    gmaps_result = {
        "results": [{"formatted_address": "test_address"}],
        "status": "OK",
    }

    return MockResponse(gmaps_result, 200)


class AddressModelTests(TestCase):
    def test_convert_query_for_gmaps(self):
        test_user = User(
            first_name="test_first_name",
            email="test@email.com",
        )

        test_date = datetime.now(tz=pytz.UTC)

        test_address = Address(
            raw_address="stary browar",
            address="Półwiejska 42, 61-888 Poznań, Poland",
            creation_date=test_date,
            owner=test_user,
        )

        self.assertEqual(
            test_address.query_address, "Półwiejska+42,+61-888+Poznań,+Poland"
        )


class ViewsTests(TestCase):
    def setUp(self) -> None:
        User = get_user_model()
        User.objects.create_user(
            "test_username", email="test@test.pl", password="password"
        )
        User.objects.create_user(
            "test_username_2", email="test2@test.pl", password="password"
        )

        self.second_users_address = Address(
            address="test_address_2",
            raw_address="raw_address_2",
            creation_date=datetime.now(tz=pytz.UTC),
            owner=User.objects.filter(username="test_username_2").get(),
        )
        self.second_users_address.save()

        self.user = User.objects.filter(username="test_username").get()

        self.assertTrue(
            self.client.login(username="test_username", password="password")
        )

    def test_add_address(self):
        with patch("requests.get", mocked_requests):
            response = self.client.post("/add_address", {"address": "stary_browar"})

        created_address = Address.objects.filter(raw_address="stary_browar").get()

        self.assertEqual("stary_browar", created_address.raw_address)
        self.assertEqual("test_address", created_address.address)
        self.assertEqual(self.user, created_address.owner)
        self.assertEqual(response.status_code, 302)

    def test_edit_address(self):
        address_to_edit = Address(
            address="test_address_old",
            raw_address="test_raw_address",
            creation_date=datetime.now(tz=pytz.UTC),
            owner=self.user,
        )
        address_to_edit.save()

        with patch("requests.get", mocked_requests):
            response = self.client.post(
                f"/edit_address/{address_to_edit.id}",
                {"address": "updated_test_address"},
            )

        updated_address = Address.objects.filter(id=address_to_edit.id).get()

        self.assertEqual("updated_test_address", updated_address.raw_address)
        self.assertEqual("test_address", updated_address.address)
        self.assertEqual(self.user, updated_address.owner)
        self.assertEqual(response.status_code, 302)

    def test_delete_address(self):
        address_to_delete = Address(
            address="test_address",
            raw_address="test_raw_address",
            creation_date=datetime.now(tz=pytz.UTC),
            owner=self.user,
        )
        address_to_delete.save()

        self.client.post("/delete_address", {"address_id": address_to_delete.id})

        with self.assertRaises(Address.DoesNotExist):
            Address.objects.filter(id=address_to_delete.id).get()

    def test_delete_someone_elses_address(self):
        response = self.client.post(
            f"/delete_address", {"address_id": self.second_users_address.id}
        )

        self.assertEqual(
            "/error/This%20address%20belongs%20to%20another%20user!", response.url
        )

    def test_edit_someone_elses_address(self):
        response = self.client.post(
            f"/edit_address/{self.second_users_address.id}", {"address": "test_eddress"}
        )

        self.assertEqual(
            "/error/This%20address%20belongs%20to%20another%20user!", response.url
        )

    def test_edit_non_existent_address(self):
        response = self.client.post(f"/edit_address/420", {"address": "test_eddress"})

        self.assertEqual("/error/This%20address%20does%20not%20exist!", response.url)

    def test_delete_non_existent_address(self):
        response = self.client.post("/delete_address", {"address_id": 420})

        self.assertEqual("/error/This%20address%20does%20not%20exist!", response.url)
