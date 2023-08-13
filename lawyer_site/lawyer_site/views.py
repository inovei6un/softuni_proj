from datetime import timedelta, datetime
from django.db import IntegrityError
from django.shortcuts import render
from django.core.mail import send_mail
from django.views import View
from lawyer_site.forms import AppointmentForm, ContactForm, DocumentForm
from lawyer_site.models import Appointment, Document


class IndexView(View):
    template_name = 'index.html'

    def get(self, request):
        return render(request, self.template_name, {})


class AboutView(View):
    template_name = 'about.html'

    def get(self, request):
        return render(request, self.template_name, {})


class PracticeView(View):
    template_name = 'practice.html'

    def get(self, request):
        documents = Document.objects.all()

        files_by_category = {
            'Гражданско право': [file for file in documents if file.category == 'Гражданско право'],
            'Семейно право': [file for file in documents if file.category == 'Семейно право'],
            'Административно право': [file for file in documents if file.category == 'Административно право'],
            'Наказателно право': [file for file in documents if file.category == 'Наказателно право'],
            'Търговско право': [file for file in documents if file.category == 'Търговско право'],
            'Трудово право': [file for file in documents if file.category == 'Трудово право'],
        }

        return render(request, self.template_name, {'files_by_category': files_by_category})


class ContactView(View):
    template_name = 'contact.html'
    success_template_name = 'contact_created.html'

    def get(self, request):
        user = request.user
        initial_data = {
            'your_name': user.first_name,
            'message_email': user.email,
        }
        form = ContactForm(initial=initial_data)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            your_name = form.cleaned_data['your_name']
            message_email = form.cleaned_data['message_email']
            message = form.cleaned_data['message']

            send_mail(
                'Консултация с/със: ' + your_name,
                f'Съобщение от {message_email}: \n\n' + message,
                message_email,
                ['advokat.r.racheva@gmail.com']
            )

            return render(request, self.success_template_name, {'your_name': your_name})

        return render(request, self.template_name, {'form': form})


class AppointmentView(View):
    template_name = 'create.html'
    success_template_name = 'appointment_created.html'

    def get(self, request):
        user = request.user
        initial_data = {
            'name': user.first_name,
            'email': user.email,
        }
        form = AppointmentForm(initial=initial_data)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = AppointmentForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            date = form.cleaned_data['date']
            time = form.cleaned_data['time']
            phone = form.cleaned_data['phone']

            datetime_obj = datetime.combine(date, time)

            time_range = datetime_obj, datetime_obj + timedelta(minutes=59)
            stringified_range = f"{datetime_obj.strftime('%H:%M:%S')} - {(datetime_obj + timedelta(minutes=59)).strftime('%H:%M:%S')}"

            # Check for existing appointments within one hour of the selected time
            existing_appointments = Appointment.objects.filter(
                date=date,
                time__range=time_range
            )

            if existing_appointments.exists():
                error_message = 'Този час вече е зает!'
                return render(request, self.template_name, {'form': form, 'error_message': error_message})

            try:
                appointment = Appointment.objects.create(
                    name=name,
                    email=email,
                    date=date,
                    time=time,

                )
                appointment.save()

                send_mail(
                    'Заявка за среща от ' + name,
                    f'Данни на заявката: \n\n Име: ' + name + f' \n Имейл: ' + email + f'\n Дата и час: ' + stringified_range + '\n Телефонен номер: ' + phone,
                    email,
                    ['advokat.r.racheva@gmail.com']
                )

                return render(request, self.success_template_name, {
                    'name': name,
                    'email': email,
                    'stringified_range': stringified_range,
                    'phone': phone
                })
            except IntegrityError:
                error_message = 'Този час вече е зает.'
                return render(request, self.template_name, {'form': form, 'error_message': error_message})
        return render(request, self.template_name, {'form': form})


def upload_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = DocumentForm()
    return render(request, 'upload_document.html', {'form': form})


# @login_required
# def deactivate_account(request):
#     user = request.user
#
#     user.is_active = False
#     user.save()
#
#     return redirect('account_deactivated.html')


def custom_404(request, exception):
    return render(request, '404.html', status=404)
