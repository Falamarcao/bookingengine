from .models import *
from rest_framework import serializers


class BookingInfoSerializer(serializers.ModelSerializer):
    listing_type = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    
    class Meta:
        model = BookingInfo
        fields = (
            'listing_type',
            'title',
            'country',
            'city',
            'price',
        )

    def get_listing_type(self, obj):
        if obj.listing == None:
            return obj.hotel_room_type.hotel.listing_type
        return obj.listing.listing_type

    def get_title(self, obj):
        if obj.listing == None:
            return obj.hotel_room_type.hotel.title
        return obj.listing.title
    
    def get_country(self, obj):
        if obj.listing == None:
            return obj.hotel_room_type.hotel.country
        return obj.listing.country
    
    def get_city(self, obj):
        if obj.listing == None:
            return obj.hotel_room_type.hotel.city
        return obj.listing.city
