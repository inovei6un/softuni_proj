from django import forms
from django.core.validators import RegexValidator, MinLengthValidator, EmailValidator

from lawyer_site.models import User
from lawyer_site.validators import validate_letters_only


class UserForm(forms.ModelForm):
    name_validator = RegexValidator(r'^[a-zA-Zа-яА-Я]+$', 'Името може да се състои само от букви!')
    first_name = forms.CharField(
        max_length=20,
        validators=[validate_letters_only, name_validator],
        label="Име",
        widget=forms.TextInput(attrs={'class': 'form-control border-0 p-4'})
    )

    last_name = forms.CharField(
        max_length=20,
        validators=[validate_letters_only, name_validator],
        label="Фамилия",
        widget=forms.TextInput(attrs={'class': 'form-control border-0 p-4'})
    )

    email = forms.EmailField(
        max_length=40,
        label="Имейл",
        widget=forms.EmailInput(attrs={'class': 'form-control border-0 p-4'})
    )

    password = forms.CharField(
        max_length=20,
        label="Парола",
        validators=[MinLengthValidator(8, message='Паролата трябва да съдържа поне 8 символа!')],
        widget=forms.PasswordInput(attrs={'class': 'form-control border-0 p-4'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']

    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email=email).exists():
            self.add_error('email', "Този имейл вече е зает. Моля, изберете друг.")

        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': 'form-control border-0 p-4', 'placeholder': 'Въведете име'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control border-0 p-4', 'placeholder': 'Въведете фамилия'})
        self.fields['email'].widget.attrs.update({'class': 'form-control border-0 p-4', 'placeholder': 'Имейл'})
        self.fields['password'].widget.attrs.update({'class': 'form-control border-0 p-4', 'placeholder': 'Въведете парола'})


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=40, label='Имейл')
    password = forms.CharField(max_length=20, widget=forms.PasswordInput, label='Парола')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control border-0 p-4', 'placeholder': 'Въведете имейл'})
        self.fields['password'].widget.attrs.update({'class': 'form-control border-0 p-4', 'placeholder': 'Въведете парола'})


class AppointmentForm(forms.Form):
    name_validator = RegexValidator(r'^[a-zA-Zа-яА-Я]+$', 'Името може да се състои само от букви!')
    name = forms.CharField(max_length=100, validators=[name_validator, MinLengthValidator(2)], label='Име')

    date_validator = RegexValidator(r'^\d{4}[/.-]\d{2}[/.-]\d{2}$', 'Форматът за дата е ГГГГ/ММ/ДД')
    date = forms.CharField(validators=[date_validator], label='Дата')

    time_validator = RegexValidator(r'^\d{2}:\d{2}$', 'Часът е във формат ЧЧ:ММ')
    time = forms.CharField(max_length=5, validators=[time_validator], label='Час')

    phone_validator = RegexValidator(r'^(\+)?\d+$', 'Телефонният номер може да съдържа само числа и "+" в началото!')
    phone = forms.CharField(max_length=20, validators=[phone_validator, MinLengthValidator(10)], label='Телефон')

    message_email_validator = EmailValidator(message='Моля въведете правилен имейл!')
    email = forms.EmailField(max_length=40, validators=[message_email_validator])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control border-0 p-4'})
        self.fields['date'].widget.attrs.update({'class': 'form-control border-0 p-4 datetimepicker-input'})
        self.fields['time'].widget.attrs.update({'class': 'form-control border-0 p-4 datetimepicker-input'})
        self.fields['phone'].widget.attrs.update({'class': 'form-control border-0 p-4 datetimepicker-input'})
        self.fields['email'].widget.attrs.update({'class': 'form-control border-0 p-4'})


class ContactForm(forms.Form):
    name_validator = RegexValidator(r'[a-zA-Zа-яА-Я]+$', 'Името може да се състои само от букви!')
    your_name = forms.CharField(label='Вашето име', max_length=100, validators=[name_validator])

    message_email_validator = EmailValidator(message='Моля въведете правилен имейл!')
    message_email = forms.EmailField(label='Имейл за контакт', max_length=100, validators=[message_email_validator])

    message = forms.CharField(label='Съобщение', widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['your_name'].widget.attrs.update({'class': 'form-control border-0 p-4', 'placeholder': 'Име'})
        self.fields['message_email'].widget.attrs.update({'class': 'form-control border-0 p-4', 'placeholder': 'Имейл'})
        self.fields['message'].widget.attrs.update({'class': 'form-control border-0 p-4', 'placeholder': 'Съобщение'})

