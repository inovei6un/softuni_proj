from django import forms
from django.core.validators import RegexValidator, MinLengthValidator, EmailValidator

from lawyer_site.models import Document
from lawyer_site.validators.date_validator import validate_date_before_today
from lawyer_site.validators.time_validator import validate_time_not_after_4pm


class AppointmentForm(forms.Form):
    name_validator = RegexValidator(r'^[a-zA-Zа-яА-Я]+$', 'Името може да се състои само от букви!')
    name = forms.CharField(max_length=20, validators=[name_validator, MinLengthValidator(2, 'Минимална дължина на име 2 букви!')], label='Име')

    date_validator = RegexValidator(r'^\d{4}[/.-]\d{2}[/.-]\d{2}$', 'Форматът за дата е ГГГГ/ММ/ДД')
    date = forms.DateField(validators=[date_validator, validate_date_before_today], label='Дата', error_messages={'invalid': 'Моля, въведете валидна дата във формат ГГГГ-ММ-ДД'})
    time = forms.TimeField(validators=[validate_time_not_after_4pm], label='Час', error_messages={'invalid': 'Моля, въведете валиден час във формат ЧЧ:ММ'})
    # date = forms.DateField(widget=SelectDateWidget(attrs={'class': 'form-control datepicker'}))
    # time = forms.TimeField(widget=forms.TimeInput(attrs={'class': 'form-control timepicker'}))
    phone_validator = RegexValidator(r'^(\+)?\d+$', 'Телефонният номер може да съдържа само числа и "+" в началото!')
    phone = forms.CharField(max_length=20, validators=[phone_validator, MinLengthValidator(10, 'Минимална дължина на телефонен номер 10 числа!')], label='Телефон')

    message_email_validator = EmailValidator(message='Моля въведете правилен имейл!')
    email = forms.EmailField(max_length=40, validators=[message_email_validator], label='Имейл')

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
        self.fields['your_name'].widget.attrs.update({'class': 'form-control border-10 p-4', 'placeholder': 'Име'})
        self.fields['message_email'].widget.attrs.update({'class': 'form-control border-10 p-4', 'placeholder': 'Имейл'})
        self.fields['message'].widget.attrs.update({'class': 'form-control border-10 p-4', 'placeholder': 'Съобщение'})


class DocumentForm(forms.ModelForm):
    title = forms.CharField(label='Заглавие', max_length=100, validators=[MinLengthValidator(5, 'Заглавието трябва да е дълго поне 5 символа!')])
    document_file = forms.FileField(label='Документ')
    category = forms.ChoiceField(label="Категория", choices=Document.CATEGORY_CHOICES)

    class Meta:
        model = Document
        fields = ['title', 'document_file', 'category']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control border-0 p-4', 'placeholder': 'Заглавие'})
        # self.fields['document_file'].widget.attrs.update({'class': 'form-control border-0 p-4', 'placeholder': 'Избери файл'})
        # self.fields['category'].widget.attrs.update({'placeholder': 'Категория'})
