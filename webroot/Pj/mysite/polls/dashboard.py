from controlcenter import Dashboard, widgets
from .models import RegisterEvent, PublishedEvent

class Customer(widgets.ItemList):
    model = RegisterEvent
    list_display = ('customer_name','attandance','customer_email')
    width = widgets.LARGE


class Event(widgets.ItemList):
    model = PublishedEvent
    list_display = ('event_name',)

class MyDashboard(Dashboard):
    widgets = (
        Customer,

    )