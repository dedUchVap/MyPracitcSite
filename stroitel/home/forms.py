import os.path
import uuid
from django.forms import *
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from home.models import *
from django import forms
from django.core.cache import cache


class RegisterForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Повторите пароль'}))
    username = forms.CharField(widget=TextInput(attrs={'placeholder': 'Имя пользователя'}))
    email = forms.CharField(widget=EmailInput(attrs={'placeholder': 'Почта'}))

    class Meta:
        model = User
        fields = ['username', 'password1', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Пользователь с таким email уже существует')
        else:
            return email


class LoginUser(AuthenticationForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}))
    username = forms.CharField(widget=TextInput(attrs={'placeholder': 'Имя пользователя'}))

    class Meta:
        model = User


class Code(Form):
    code = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Код подтверждения'}))

    def clean_code(self):
        code = self.cleaned_data.get('code')
        email = self.data['email']
        if code == cache.get(email):
            return True
        else:
            raise ValidationError('Код неверный,либо время его действия истекло')


class BidForm(ModelForm):
    communication_method_list = [
        ('', 'Выбор связи'),
        ('Telegram', 'Telegram'),
        ('Viber', 'Viber'),
        ('Whatsapp', 'Whatsapp'),
        ('Email', 'Email'),
    ]
    number_phones = forms.CharField(widget=TextInput(attrs={'placeholder': 'Номер телефона'}))
    smeta_path = forms.FileField(widget=forms.FileInput({'id': 'smeta'}))
    communication_method = forms.ChoiceField(widget=Select(attrs={'class': 'section-be'}), choices=communication_method_list)

    class Meta():
        model = Bid
        fields = ['number_phones', 'smeta_path', 'communication_method']

    def clean_smeta_path(self):
        os.makedirs('smeta/', exist_ok=True)
        file = self.cleaned_data.get('smeta_path')
        file_path = os.path.join('smeta/', f'{uuid.uuid4()}_{file.name}')

        with open(file_path, 'wb+') as ready_file:
            for chunk in file.chunks():
                ready_file.write(chunk)

        return file_path
