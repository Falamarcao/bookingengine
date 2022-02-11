from .models import BookingInfo, Reservation
from .serializers import BookingInfoSerializer
from .utils import str_to_datetime
from django.db.models import Min
from rest_framework import response, serializers, views


class Units(views.APIView):
    """
    Get available Apartments and Hotels based on:
        - Star Date: 2021-12-09
        - End Date: 2021-12-12
        - Max Price: integer > 0.

        e.g. /api/v1/units/?max_price=100&check_in=2021-12-09&check_out=2021-12-12

    """

    def get(self, request):

        try:

            # Query URL params
            check_in = str_to_datetime(self.request.query_params.get('check_in', None))
            check_out = str_to_datetime(self.request.query_params.get('check_out', None))
            max_price = self.request.query_params.get('max_price', None)

            # Checking reservations from requested date range
            reservations_ids = Reservation.objects.filter(check_in__range=(check_in, check_out)).values('booking_info__id')                                                          \
                           &   \
                           Reservation.objects.filter(check_out__range=(check_in, check_out)).values('booking_info__id')

            # Excluding blocked places
            booking_info = BookingInfo.objects.exclude(id__in=reservations_ids)

            # max_price filter
            if max_price:
                booking_info = booking_info.filter(price__lte=int(max_price))

            # Only the cheapest HotelRoomType with available HotelRoom
            cheapest = booking_info.values('hotel_room_type__hotel').annotate(Min('price'))
        
            booking_info = booking_info.filter(price__in=cheapest.values_list('price__min', flat=True))  \
                           |    \
                           booking_info.exclude(listing__isnull=True) # keep apartments: they has 'listing' not null

            return response.Response({'items': BookingInfoSerializer(booking_info, many=True).data})
       
        except ValueError:
            raise serializers.ValidationError('Value Error, you should check the URL params.')

        except Exception as e:
            raise serializers.ValidationError(e)
