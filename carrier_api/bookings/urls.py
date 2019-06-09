from django.conf.urls import include
from django.urls import path

from carrier_api.bookings import views


urlpatterns = [
    path('', views.api_root),

    path('aircrafts/', include([
        path('', views.AircraftsListCreateView.as_view(), name='aircrafts-list'),
        path('<aircraft_code>', views.AircraftsRetrieveUpdateDestroyView.as_view(), name='aircrafts-detail')
    ])),

    path('airports/', include([
        path('', views.AirportsListCreateView.as_view(), name='airports-list'),
        path('<airport_code>', views.AirportsRetrieveUpdateDestroyView.as_view(), name='airports-detail'),
    ])),

    path('bookings/', include([
        path('', views.BookingsListCreateView.as_view(), name='bookings-list'),
        path('<book_ref>', views.BookingsRetrieveUpdateDestroyView.as_view(), name='bookings-detail'),
    ])),

    path('boarding-passes/', include([
        path('', views.BoardingPassesListCreateView.as_view(), name='boardingpasses-list'),
        path('<ticket_no>/<flight_id>', views.BoardingPassesRetrieveDestroyView.as_view(),
             name='boardingpasses-detail'),
    ])),

    path('flights/', include([
        path('', views.FlightsListCreateView.as_view(), name='flights-list'),
        path('<flight_id>', views.FlightsRetrieveUpdateDestroyView.as_view(), name='flights-detail'),
    ])),

    path('tickets/', include([
        path('', views.TicketsListCreateView.as_view(), name='tickets-list'),
        path('<ticket_no>', views.TicketsRetrieveUpdateDestroyView.as_view(), name='tickets-detail'),
    ])),

    path('ticket-flights/', include([
        path('', views.TicketFlightsListCreateView.as_view(), name='ticketflights-list'),
        path('<ticket_no>/<flight>', views.TicketFlightsRetrieveDestroyView.as_view(), name='ticketflights-detail')
    ])),

    path('seats/', include([
        path('', views.SeatsListCreateView.as_view(), name='seats-list'),
        path('<aircraft_code>/<seat_no>', views.SeatsRetrieveDestroyView.as_view(), name='seats-detail')
    ]))
]
