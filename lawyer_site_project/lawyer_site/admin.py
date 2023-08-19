from django.contrib import admin
from lawyer_site.models import Appointment, Document


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'date', 'time')


admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Document)
