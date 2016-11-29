from django.conf.urls import url
from .views import LoginView,LogoutView

urlpatterns = [
    url(r'login/$',LoginView.as_view(), name='rest_login'),
    url(r'logout/$',LogoutView.as_view(),name='rest_logout'),
]