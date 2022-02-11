from ..models import *
from string import digits
from factory import django, Faker, SubFactory, fuzzy
from datetime import datetime

class ListingFactory(django.DjangoModelFactory):
    class Meta:
        model = Listing
    
    listing_type = fuzzy.FuzzyChoice([x[0] for x in Listing.LISTING_TYPE_CHOICES])
    title = Faker('catch_phrase')
    country = Faker('country')
    city = Faker('city')


class HotelRoomTypeFactory(django.DjangoModelFactory):
    class Meta:
        model = HotelRoomType

    hotel = SubFactory(ListingFactory)
    title = fuzzy.FuzzyChoice(['Double Room', 'Double Room Deluxe', 
    'Single Room', 'Single Room Deluxe', 'Family Room', 'Triple Room'])


class HotelRoomFactory(django.DjangoModelFactory):
    class Meta:
        model = HotelRoom

    hotel_room_type = SubFactory(HotelRoomTypeFactory)
    room_number = fuzzy.FuzzyText(length=3, chars=digits)


class BookingInfoFactory(django.DjangoModelFactory):
    class Meta:
        model = BookingInfo

    listing = SubFactory(ListingFactory)
    hotel_room_type = SubFactory(HotelRoomTypeFactory)
    price = fuzzy.FuzzyDecimal(1.00, 200.00)

class ReservationFactory(django.DjangoModelFactory):
    class Meta:
        model = Reservation
        django_get_or_create = ('booking_info',)

    booking_info = BookingInfo.objects.filter(pk=4)[0]
    check_in = datetime(2021,12,9)
    check_out = datetime(2022,12,12)
