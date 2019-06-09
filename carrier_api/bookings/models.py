from _decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.postgres.fields import JSONField


class Aircrafts(models.Model):
    """
    Модель: Літак
    """
    aircraft_code = models.CharField(primary_key=True, max_length=3)
    model = JSONField()
    range = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        managed = False
        db_table = 'aircrafts_data'


class Airports(models.Model):
    """
    Модель: Аейропорт
    """
    airport_code = models.CharField(primary_key=True, max_length=3)
    airport_name = JSONField()
    city = JSONField()
    coordinates = models.TextField()  # This field type is a guess. JSONField()
    timezone = models.TextField()

    class Meta:
        managed = False
        db_table = 'airports_data'


class Bookings(models.Model):
    """
    Модель: Бронювання
    """
    book_ref = models.CharField(primary_key=True, max_length=6)
    book_date = models.DateTimeField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'bookings'


class Flights(models.Model):
    """
    Модель: Рейс
    """
    FLIGHTS_STATUSES_CHOICES = (
        ('Scheduled', 'Scheduled'),
        ('On Time', 'On Time'),
        ('Delayed', 'Delayed'),
        ('Departed', 'Departed'),
        ('Arrived', 'Arrived'),
        ('Cancelled', 'Cancelled')
    )

    flight_id = models.AutoField(primary_key=True)
    flight_no = models.CharField(max_length=6)
    scheduled_departure = models.DateTimeField()
    scheduled_arrival = models.DateTimeField()
    departure_airport = models.ForeignKey(
        Airports, models.DO_NOTHING,
        db_column='departure_airport',
        related_name='departure_airport'
    )
    arrival_airport = models.ForeignKey(
        Airports, models.DO_NOTHING,
        db_column='arrival_airport',
        # related_name='arrival_airport'
    )
    status = models.CharField(max_length=20, choices=FLIGHTS_STATUSES_CHOICES)
    aircraft_code = models.ForeignKey(Aircrafts, models.DO_NOTHING, db_column='aircraft_code')
    actual_departure = models.DateTimeField(blank=True, null=True)
    actual_arrival = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'flights'
        unique_together = (('flight_no', 'scheduled_departure'),)


class Seats(models.Model):
    """
    Модель: Місце
    """
    FARE_CONDITIONS_CHOICES = (
        ('Economy', 'Economy'),
        ('Comfort', 'Comfort'),
        ('Business', 'Business')
    )

    aircraft_code = models.ForeignKey(Aircrafts, models.DO_NOTHING, db_column='aircraft_code', primary_key=True)
    seat_no = models.CharField(max_length=4)
    fare_conditions = models.CharField(max_length=10, choices=FARE_CONDITIONS_CHOICES)

    class Meta:
        managed = False
        db_table = 'seats'
        unique_together = (('aircraft_code', 'seat_no'),)


class Tickets(models.Model):
    """
    Модель: Квитків
    """
    ticket_no = models.CharField(primary_key=True, max_length=13)
    book_ref = models.ForeignKey(Bookings, models.DO_NOTHING, db_column='book_ref')
    passenger_id = models.CharField(max_length=20)
    passenger_name = models.TextField()
    contact_data = JSONField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tickets'


class TicketFlights(models.Model):
    """
    Модель: Політ (літака)
    """
    ticket_no = models.ForeignKey('Tickets', models.DO_NOTHING, db_column='ticket_no', primary_key=True)
    flight = models.ForeignKey(Flights, models.DO_NOTHING)
    fare_conditions = models.CharField(max_length=10)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])

    class Meta:
        managed = False
        db_table = 'ticket_flights'
        unique_together = (('ticket_no', 'flight'),)


class BoardingPasses(models.Model):
    """
    Модель: Талону посадки
    """
    ticket_no = models.ForeignKey('TicketFlights', models.DO_NOTHING, db_column='ticket_no', primary_key=True)
    flight_id = models.IntegerField()
    boarding_no = models.IntegerField()
    seat_no = models.CharField(max_length=4)

    class Meta:
        managed = False
        db_table = 'boarding_passes'
        unique_together = (('flight_id', 'boarding_no'), ('flight_id', 'seat_no'), ('ticket_no', 'flight_id'),)