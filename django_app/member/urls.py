from django.conf.urls import url
from .views import LoginView,LogoutView, UserDetailsView

urlpatterns = [
    url(r'^login/$',LoginView.as_view(), name='rest_login'),
    url(r'^logout/$',LogoutView.as_view(),name='rest_logout'),
    url(r'^user/$',UserDetailsView.as_view(),name='userdetail'),
    ]