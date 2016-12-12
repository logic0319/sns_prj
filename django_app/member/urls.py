from django.conf.urls import url

from member.views.alarm import AlarmListView, AlarmDeleteView
from .views import LoginView, LogoutView, RegisterView, UserUpdateView, EmailVerifyingView, PasswordSendView, PasswordChangeView

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='rest_login'),
    url(r'^logout/$', LogoutView.as_view(), name='rest_logout'),
    url(r'^signup/$', RegisterView.as_view(), name='rest_register'),
    url(r'^update/(?P<pk>\d+)/$', UserUpdateView.as_view(), name='user_update'),
    url(r'^send_pw/(?P<email>[0-9a-zA-Z_\-]+@[.0-9a-zA-Z_\-]+)/$', PasswordSendView.as_view(), name='password_send'),
    url(r'^change_pw/$', PasswordChangeView.as_view(), name='change_password'),
    url(r'^email_verify/(?P<hash>[\w]+)/$', EmailVerifyingView.as_view(), name='user_update'),
    url(r'^alarm/$', AlarmListView.as_view(), name='alarm_list'),
    url(r'^alarm/(?P<pk>\d+)/delete/$', AlarmDeleteView.as_view(), name='alarm_delete'),
]
