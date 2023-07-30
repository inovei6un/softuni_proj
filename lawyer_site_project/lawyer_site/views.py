from django.contrib.auth import login, authenticate
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.views import View
from lawyer_site.forms import AppointmentForm, ContactForm, UserForm, LoginForm
from lawyer_site.models import Appointment


def register_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user instance
            login(request, user)  # Log in the user
            return redirect("index")
    else:
        form = UserForm()

    return render(request, 'register.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("index")
            else:
                error_message = "Невалидни данни за вход. Моля, опитайте отново."
                return render(request, 'login.html', {'form': form, 'error_message': error_message})
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


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
        return render(request, self.template_name, {})


class ContactView(View):
    template_name = 'contact.html'
    success_template_name = 'contact_created.html'

    def get(self, request):
        form = ContactForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            your_name = form.cleaned_data['your_name']
            message_email = form.cleaned_data['message_email']
            message = form.cleaned_data['message']

            send_mail(
                'Консултация от: ' + your_name,
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
        form = AppointmentForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = AppointmentForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            date = form.cleaned_data['date']
            time = form.cleaned_data['time']
            phone = form.cleaned_data['phone']
            try:
                appointment = Appointment.objects.create(
                    name=name,
                    email=email,
                    date=date,
                    time=time,
                    # phone=phone
                )
                appointment.save()
                send_mail(
                    'Заявка за среща от ' + name,
                    f'Данни на заявката: \n\n Име: ' + name + f' \n Имейл: ' + email + f'\n Дата: ' + date + f'\n Час: ' + time + '\n Телефонен номер: ' + phone,
                    email,
                    ['advokat.r.racheva@gmail.com']
                )

                return render(request, self.success_template_name, {
                    'name': name,
                    'email': email,
                    'date': date,
                    'time': time,
                    'phone': phone
                })
            except IntegrityError:
                error_message = 'Този час вече е зает.'
                return render(request, self.template_name, {'form': form, 'error_message': error_message})
        return render(request, self.template_name, {'form': form})
