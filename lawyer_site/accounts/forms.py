from django import forms
from django.core.validators import MinLengthValidator
from accounts.models import CustomUser
from lawyer_site.validators.password_validator import validate_common_password


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Парола', validators=[MinLengthValidator(8, message='Паролата трябва да съдържа поне 8 символа!'), validate_common_password])
    repeat_password = forms.CharField(widget=forms.PasswordInput, label='Повторете Паролата')

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password', 'repeat_password']
        labels = {
            'first_name': 'Име',
            'last_name': 'Фамилия',
            'email': 'Имейл',
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        repeat_password = cleaned_data.get('repeat_password')
        if password and repeat_password and password != repeat_password:
            raise forms.ValidationError("Паролите не съвпадат!")

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': 'form-control border-0 p-4', 'placeholder': 'Въведете име'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control border-0 p-4', 'placeholder': 'Въведете фамилия'})
        self.fields['email'].widget.attrs.update({'class': 'form-control border-0 p-4', 'placeholder': 'Имейл'})
        self.fields['password'].widget.attrs.update({'class': 'form-control border-0 p-4', 'placeholder': 'Въведете парола'})
        self.fields['repeat_password'].widget.attrs.update({'class': 'form-control border-0 p-4', 'placeholder': 'Повторете паролата'})
        self.fields['email'].error_messages.update({'unique': "Потребител с такъв имейл вече съществува!"})


class UserLoginForm(forms.Form):
    email = forms.EmailField(label='Имейл')
    password = forms.CharField(widget=forms.PasswordInput, label='Парола')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control border-0 p-4', 'placeholder': 'Въведете имейл'})
        self.fields['email'].error_messages.update({'invalid': "Моля въведете валиден имейл адрес!"})
        self.fields['password'].widget.attrs.update({'class': 'form-control border-0 p-4', 'placeholder': 'Въведете парола'})


class UserProfileForm(UserRegistrationForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password', 'repeat_password']
        labels = {
            'first_name': 'Име',
            'last_name': 'Фамилия',
            'email': 'Имейл',
            'password': 'Парола',
            'repeat_password': 'Повторете Паролата',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': 'form-control border-0 p-4', 'placeholder': 'Въведете име'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control border-0 p-4', 'placeholder': 'Въведете фамилия'})
        self.fields['email'].widget.attrs.update({'class': 'form-control border-0 p-4', 'placeholder': 'Имейл'})
        self.fields['password'].widget.attrs.update({'class': 'form-control border-0 p-4', 'placeholder': 'Въведете парола'})
        self.fields['repeat_password'].widget.attrs.update({'class': 'form-control border-0 p-4', 'placeholder': 'Повторете паролата'})
