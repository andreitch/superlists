from django.conf.urls import url
from accounts import views

urlpatterns = [
    url(r'^login$', views.login, name='login'),
    url(r'^send_login_email$', views.send_login_email, name='send_login_email'),
]
