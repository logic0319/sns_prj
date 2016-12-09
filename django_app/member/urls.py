from django.conf.urls import url
from .views import LoginView, LogoutView, RegisterView, UserUpdateView, EmailVerifyingView

urlpatterns = [
    url(r'login/$',LoginView.as_view(), name='rest_login'),
    url(r'logout/$',LogoutView.as_view(),name='rest_logout'),
    url(r'signup/$', RegisterView.as_view(), name='rest_register'),
    url(r'update/(?P<pk>\d+)/$', UserUpdateView.as_view(), name='user_update'),
    url(r'email_verify/(?P<hash>[\w]+)/$', EmailVerifyingView.as_view(), name='user_update'),
]
