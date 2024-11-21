import json
from django.core.mail import send_mail
from django.views.generic import *
from home.utils import *
from home.forms import *
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.http import JsonResponse
from django.core.cache import cache
from django.contrib import messages
from django.shortcuts import reverse


class Home(DataMixin, TemplateView):
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная'

        return context


class Profile(Aut, DataMixin, CreateView):
    model = Bid
    form_class = BidForm
    template_name = 'profile/profile.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Прфоиль'
        context['user'] = self.request.user

        return context

    def form_valid(self, form):
        form.instance.people = self.request.user
        send_mail(
            subject='Заявка "БИК-МОНТАЖ"',
            message='.',
            from_email='efimencko14@yandex.ru',
            recipient_list=[self.request.user.email],
            html_message=message_for_bid
        )
        return super().form_valid(form)


class Login(DataMixin, LoginView):
    template_name = 'login/login.html'
    form_class = LoginUser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Вход'
        return context

    def get_success_url(self):
        return reverse_lazy('home')


class Register(DataMixin, TemplateView):
    template_name = 'register/register.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        context['form_one'] = RegisterForm
        context['form_two'] = Code
        return context

    @staticmethod
    def get_success_url(self):
        return reverse_lazy('home')


def logout_my(request):
    logout(request)
    return redirect('home')


class SubmitRegister(View):

    def post(self, request, *args, **kwargs):
        user_form = RegisterForm(json.loads(request.body))
        if user_form.is_valid():
            if cache.get('email'):
                return JsonResponse({'status': False, 'errors': {'code_fail': "Код уже был отправлен"}}, status=400)
            data = json.loads(request.body)
            code_for_email = key_generate()
            cache.set(data['email'], code_for_email, timeout=300)
            cache.set(data['username'], data, timeout=600)
            send_mail(
                'Код',
                f'',
                'efimencko14@ya.ru',
                [data['email']],
                html_message=message_for_code + code_for_email

            )
            return JsonResponse({'status': True})
        else:
            return JsonResponse({'status': False, 'errors': user_form.errors}, status=400)


class CodeConfirm(View):

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        form = Code(data)
        user_data = cache.get(data['username'])
        if form.is_valid():
            try:
                user_form = RegisterForm(user_data)
                user_form.save()
                messages.success(request, 'Вы успешно зарегистрировались')
                return redirect(reverse('login'))
            except Exception as e:
                print(e)
                return JsonResponse({'status': 'db_no cool', 'errors': form.errors}, status=400)
        else:
            return JsonResponse({'status': 'bad', 'errors': form.errors}, status=400)
