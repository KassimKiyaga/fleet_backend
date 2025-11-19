from django.contrib import admin

# Registeration of our models.
from django.contrib import admin
from .models import Vehicle, Driver, Booking, Trip, Feedback, MaintenanceRecord, FuelRecord, Incident, Department

admin.site.register(Vehicle)
admin.site.register(Driver)
admin.site.register(Booking)
admin.site.register(Trip)
admin.site.register(Feedback)
admin.site.register(MaintenanceRecord)
admin.site.register(FuelRecord)
admin.site.register(Incident)
admin.site.register(Department)
