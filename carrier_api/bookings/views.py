from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from carrier_api.bookings.mixins import MultipleFieldLookupMixin
from .models import Bookings, Aircrafts, Airports, Flights, Seats, BoardingPasses, TicketFlights, Tickets
from .serializers import BookingsSerializer, AircraftsSerializer, AirportsSerializer, FlightsSerializer, \
    SeatsSerializer, BoardingPassesSerializer, TicketFlightsSerializer, TicketsSerializer


@api_view(['GET'])
def api_root(request, format=None):
    """
    Посилання API
    """
    return Response({
        'aircrafts': reverse('aircrafts-list', request=request, format=format),
        'airports': reverse('airports-list', request=request, format=format),
        'bookings': reverse('bookings-list', request=request, format=format),
        'booking-passes': reverse('boardingpasses-list', request=request, format=format),
        'flights': reverse('flights-list', request=request, format=format),
        'tickets': reverse('tickets-list', request=request, format=format),
        'ticket-flights': reverse('ticketflights-list', request=request, format=format),
        'seats': reverse('seats-list', request=request, format=format)
    })


class AircraftsListCreateView(generics.ListCreateAPIView):
    """
    Відображення списку та створення моделі Літак
    """
    serializer_class = AircraftsSerializer
    queryset = Aircrafts.objects.all()


class AircraftsRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Перегляд, редагування, видалення моделі Літак
    """
    queryset = Aircrafts.objects.all()
    serializer_class = AircraftsSerializer
    lookup_field = 'aircraft_code'


class AirportsListCreateView(generics.ListCreateAPIView):
    """
    Відображення списку та створення моделі Аейропорт
    """
    serializer_class = AirportsSerializer
    queryset = Airports.objects.all()


class AirportsRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Перегляд, редагування, видалення моделі Аейропорт
    """
    serializer_class = AirportsSerializer
    queryset = Airports.objects.all()
    lookup_field = 'airport_code'


class BookingsListCreateView(generics.ListCreateAPIView):
    """
    Відображення списку та створення моделі Бронювання
    """
    serializer_class = BookingsSerializer
    queryset = Bookings.objects.all()


class BookingsRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Перегляд, редагування, видалення моделі Бронювання
    """
    serializer_class = BookingsSerializer
    queryset = Bookings.objects.all()
    lookup_field = 'book_ref'


class TicketsListCreateView(generics.ListCreateAPIView):
    """
    Відображення списку та створення моделі Квиток
    """
    serializer_class = TicketsSerializer
    queryset = Tickets.objects.all()


class TicketsRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Перегляд, редагування, видалення моделі Квиток
    """
    serializer_class = TicketsSerializer
    queryset = Tickets.objects.all()
    lookup_field = 'ticket_no'


class TicketFlightsListCreateView(generics.ListCreateAPIView):
    """
    Відображення списку та створення моделі Політ (літака)
    """
    serializer_class = TicketFlightsSerializer
    queryset = TicketFlights.objects.all()


class TicketFlightsRetrieveDestroyView(MultipleFieldLookupMixin, generics.RetrieveDestroyAPIView):
    """
    Перегляд, видалення моделі Політ (літака)
    """
    serializer_class = TicketFlightsSerializer
    queryset = TicketFlights.objects.all()
    multiple_lookup_fields = ['ticket_no', 'flight']


class BoardingPassesListCreateView(generics.ListCreateAPIView):
    """
    Відображення списку та створення моделі Талон посадки
    """
    serializer_class = BoardingPassesSerializer
    queryset = BoardingPasses.objects.all()


class BoardingPassesRetrieveDestroyView(MultipleFieldLookupMixin, generics.RetrieveDestroyAPIView):
    """
    Перегляд, видалення моделі Талон посадки
    """
    queryset = BoardingPasses.objects.all()
    serializer_class = BoardingPassesSerializer
    multiple_lookup_fields = ('ticket_no', 'flight_id')


class FlightsListCreateView(generics.ListCreateAPIView):
    """
    Відображення списку та створення моделі Рейсу
    """
    serializer_class = FlightsSerializer
    queryset = Flights.objects.all()


class FlightsRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Перегляд, редагування, видалення моделі Рейсу
    """
    serializer_class = FlightsSerializer
    queryset = Flights.objects.all()
    lookup_field = 'flight_id'


class SeatsListCreateView(generics.ListCreateAPIView):
    """
    Відображення списку та створення моделі Місце
    """
    serializer_class = SeatsSerializer
    queryset = Seats.objects.all()


class SeatsRetrieveDestroyView(MultipleFieldLookupMixin, generics.RetrieveDestroyAPIView):
    """
    Перегляд, видалення моделі Місце
    """
    queryset = Seats.objects.all()
    serializer_class = SeatsSerializer
    multiple_lookup_fields = ['aircraft_code', 'seat_no']
