from django.conf.urls import url

from member.views import RegisterView

urlpatterns = [
    # url(r'^member/', include('rest_auth.urls')),
    url(r'^$', RegisterView.as_view(), name='rest_register'),
]
