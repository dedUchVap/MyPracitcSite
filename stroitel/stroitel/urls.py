from django.contrib import admin
from django.urls import path, include
from home.views import *
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Home.as_view(), name='home'),
    path('profile/', Profile.as_view(), name='profile'),
    path('login/', Login.as_view(), name='login'),
    path('register/', Register.as_view(), name='register'),
    path('logout/', logout_my, name='logout'),
    path('submit_register/', SubmitRegister.as_view(), name='submit_register'),
    path('code/', CodeConfirm.as_view(), name='code')
]
urlpatterns += debug_toolbar_urls()