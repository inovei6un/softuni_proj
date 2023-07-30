from django.contrib import admin
from lawyer_site.models import Appointment


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'appointment_datetime', 'phone')


admin.site.register(Appointment)
