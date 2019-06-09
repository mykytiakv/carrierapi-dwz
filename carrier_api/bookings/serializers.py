from rest_framework import serializers

from carrier_api.bookings.utils import ParameterisedHyperlinkedIdentityField
from .models import Bookings, Aircrafts, Airports, Flights, BoardingPasses, Seats, Tickets, TicketFlights


class AircraftsSerializer(serializers.HyperlinkedModelSerializer):
    """
    Серіалайзер моделі Літак
    """
    url = ParameterisedHyperlinkedIdentityField(
        view_name='aircrafts-detail',
        lookup_fields=(('aircraft_code', 'aircraft_code'),),
        read_only=True
    )

    class Meta:
        model = Aircrafts
        fields = '__all__'


class AirportsSerializer(serializers.HyperlinkedModelSerializer):
    """
    Серіалайзер моделі Аейропорт
    """
    url = ParameterisedHyperlinkedIdentityField(
        view_name='airports-detail',
        lookup_fields=(('airport_code', 'airport_code'),),
        read_only=True
    )

    class Meta:
        model = Airports
        fields = '__all__'


class BookingsSerializer(serializers.HyperlinkedModelSerializer):
    """
    Серіалайзер моделі Бронювання
    """
    url = ParameterisedHyperlinkedIdentityField(
        view_name='bookings-detail',
        lookup_fields=(('book_ref', 'book_ref'),),
        read_only=True
    )

    class Meta:
        model = Bookings
        fields = '__all__'


class BoardingPassesSerializer(serializers.HyperlinkedModelSerializer):
    """
    Серіалайзер моделі Талону посадки
    """
    url = ParameterisedHyperlinkedIdentityField(
        view_name='boardingpasses-detail',
        lookup_fields=(('ticket_no_id', 'ticket_no'), ('flight_id', 'flight_id')),
        read_only=True
    )

    class Meta:
        model = BoardingPasses
        fields = ('url', 'ticket_no', 'flight_id', 'boarding_no', 'seat_no')


class FlightsSerializer(serializers.ModelSerializer):
    """
    Серіалайзер моделі Рейсу
    """
    url = ParameterisedHyperlinkedIdentityField(
        view_name='flights-detail',
        lookup_fields=(('flight_id', 'flight_id'),),
        read_only=True
    )
    departure_airport = serializers.PrimaryKeyRelatedField(queryset=Airports.objects.all())
    arrival_airport = serializers.PrimaryKeyRelatedField(queryset=Airports.objects.all())
    aircraft_code = serializers.PrimaryKeyRelatedField(queryset=Aircrafts.objects.all())

    class Meta:
        model = Flights
        fields = '__all__'

    def validate(self, data):
        if data['scheduled_arrival'] < data['scheduled_departure']:
            raise serializers.ValidationError("Дата вилету не може бути швидчою за дату прибуття")

        if data['actual_departure'] is not None and data['actual_arrival'] is not None:
            if data['actual_departure'] > data['actual_arrival']:
                raise serializers.ValidationError("Факт. дата прибуття не може бути швидчою за факт. дату вилету")
        return data


class SeatsSerializer(serializers.ModelSerializer):
    """
    Серіалайзер моделі Місця
    """
    url = ParameterisedHyperlinkedIdentityField(
        view_name='seats-detail',
        lookup_fields=(('aircraft_code_id', 'aircraft_code'), ('seat_no', 'seat_no')),
        read_only=True
    )
    aircraft_code = serializers.PrimaryKeyRelatedField(queryset=Aircrafts.objects.all())

    class Meta:
        model = Seats
        fields = '__all__'


class TicketsSerializer(serializers.HyperlinkedModelSerializer):
    """
    Серіалайзер моделі Квитку
    """
    url = ParameterisedHyperlinkedIdentityField(
        view_name='tickets-detail',
        lookup_fields=(('ticket_no', 'ticket_no'),),
        read_only=True
    )
    book_ref = ParameterisedHyperlinkedIdentityField(
        view_name='bookings-detail',
        lookup_fields=(('book_ref.book_ref', 'book_ref'),),
        read_only=True
    )

    class Meta:
        model = Tickets
        fields = '__all__'


class TicketFlightsSerializer(serializers.ModelSerializer):
    """
    Серіалайзер моделі Польту (літака)
    """
    url = ParameterisedHyperlinkedIdentityField(
        view_name='ticketflights-detail',
        lookup_fields=(('ticket_no.ticket_no', 'ticket_no'), ('flight.flight_id', 'flight')),
        read_only=True
    )
    ticket_no = serializers.PrimaryKeyRelatedField(queryset=Tickets.objects.all())
    flight = serializers.PrimaryKeyRelatedField(queryset=Flights.objects.all())
    fare_conditions = serializers.CharField()
    amount = serializers.CharField()

    class Meta:
        model = TicketFlights
        fields = '__all__'
