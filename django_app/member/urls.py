from django.conf.urls import url

from member.views import RegisterView

urlpatterns = [
    url(r'^$', RegisterView.as_view(), name='rest_register'),
]
