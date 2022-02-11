from ..models import Reservation
from .factory_models import BookingInfoFactory, ReservationFactory
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from json import dumps

class UnitApiTest(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.booking_info_object = BookingInfoFactory.build()
        
        # Create entries on database
        cls.n = 4
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

    # Error expected
    def test_dateformat(self):
        data = {
            'max_price': 'HIGH',
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

    # Sucess expected
    def test(self):
        data = {
            'max_price': 20,
            'check_in': '2021-12-09',
            'check_out': '2021-12-12'
        }
        response = self.client.get(self.api_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Is max_price working?
            # Do response has less items than number of created items?
        self.assertTrue(len(response.data['items']) < self.n)
