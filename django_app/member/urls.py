from django.conf.urls import url
from .views import LoginView, LogoutView, RegisterView, UserUpdateView, PasswordSendView, PasswordChangeView

urlpatterns = [
    url(r'login/$',LoginView.as_view(), name='rest_login'),
    url(r'logout/$',LogoutView.as_view(),name='rest_logout'),
    url(r'signup/$', RegisterView.as_view(), name='rest_register'),
    url(r'update/(?P<pk>\d+)/$', UserUpdateView.as_view(), name='user_update'),
    url(r'send_pw/(?P<email>[0-9a-zA-Z_\-]+@[.0-9a-zA-Z_\-]+)/$', PasswordSendView.as_view(), name='password_send'),
    url(r'change_pw/$', PasswordChangeView.as_view(), name='change_password'),
]
