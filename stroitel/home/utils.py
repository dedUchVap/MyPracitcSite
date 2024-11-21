from django.utils.safestring import mark_safe
import secrets
import string
from django.shortcuts import redirect
from django.contrib import messages

menu = [{'title': 'Главная', 'url_name': 'home'},
        {'title': 'Оставить заяву', 'url_name': 'profile'},
        {'title': 'Регистрация', 'url_name': 'register'},
        {'title': 'Вход', 'url_name': 'login'}]

message_for_bid = mark_safe(
    '<h3>Здравствуйте, мы получили вашу заявку</h3> <br> Она будет рассмотрена в ближайщее время, с вам свяжутся по указаномму способу связи, <br> если возникнут вопросы, звоните по горячей линии, на эту почту будут приходить данны о статусе вашей заявки и т.д')

message_for_code = mark_safe('<h3>Ваш код подтверждения для регистрации</h3>Для завершения регистрации, вам нужно вернуться на страницу и вввести код, указаный ниже <br> <h4>Ваш код подтверждения - </h4>')
class DataMixin:

    def get_context_data(self, **kwargs):
        menu_copy = menu.copy()
        if self.request.user.is_authenticated:
            menu_copy.pop(2)
            menu_copy.pop(2)
            menu_copy.append({'title': 'Выход', 'url_name': 'logout'})

        context = super().get_context_data(**kwargs)
        context['menu'] = menu_copy

        return context


class Aut:
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.warning(request, 'Для входа в профиль нужно войти в аккаунт')
            return redirect('login')
        return super().dispatch(request, *args, *kwargs)


def key_generate():
    characters = string.digits + string.ascii_lowercase + string.ascii_uppercase
    code_for_email = ''.join(secrets.choice(characters) for _ in range(0, 6))
    return code_for_email
