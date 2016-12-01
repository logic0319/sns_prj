from django.conf.urls import url
from .views import LoginView,LogoutView,RegisterView,UserDetailView

urlpatterns = [
    url(r'login/$',LoginView.as_view(), name='rest_login'),
    url(r'logout/$',LogoutView.as_view(),name='rest_logout'),
    url(r'signup/$', RegisterView.as_view(), name='rest_register'),
    url(r'userdetail/$',UserDetailView.as_view(),name='user_detail')
]
