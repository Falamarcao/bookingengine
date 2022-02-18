from ..models import Reservation
from .utils import check_limit, json_to_file
from .factory_models import BookingInfoFactory, ReservationFactory
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status



class UnitApiTest(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.booking_info_object = BookingInfoFactory.build()
        
        # Create entries on database
        cls.n = 10
        cls.booking_info_create = BookingInfoFactory.create_batch(cls.n)

        # Create 1 reservation
        cls.reervation_create = ReservationFactory.create()

        cls.client = APIClient()
        cls.api_url = reverse('api:units')

    # Error expected
    def test_dateformat(self):
        data = {
            'max_price': 200,
            'check_in': '2021/12/09',
            'check_out': '2021-12-12'
        }
        response = self.client.get(self.api_url, data, format='json')
        self.assertEqual(response.data[0], 'Value Error, you should check the URL params.')

    # Sucess expected
    def test_no_max_price(self):
        data = {
            'check_in': '2021-12-09',
            'check_out': '2021-12-12'
        }
        response = self.client.get(self.api_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        json_to_file(response.data, f'test_no_max_price')

    def test_one(self):
        data = {
            'max_price': 50,
            'check_in': '2021-12-09',
            'check_out': '2021-12-12'
        }
        response = self.client.get(self.api_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)      
        
        self.assertTrue(check_limit(response.data, 'price', 50))

        json_to_file(response.data, f'test_max_price_{data["max_price"]}')

    def test_two(self):
        data = {
            'max_price': 60,
            'check_in': '2021-12-09',
            'check_out': '2021-12-12'
        }
        response = self.client.get(self.api_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertTrue(check_limit(response.data, 'price', 60))

        json_to_file(response.data, f'test_max_price_{data["max_price"]}')

    def test_three(self):
        data = {
            'max_price': 200,
            'check_in': '2021-12-09',
            'check_out': '2021-12-12'
        }
        response = self.client.get(self.api_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertTrue(check_limit(response.data, 'price', 200))

        json_to_file(response.data, f'test_max_price_{data["max_price"]}')

