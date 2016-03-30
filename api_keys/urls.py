from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .views import APIKeyListView, APIKeyDeleteView

urlpatterns = [
    url(
        r'^keys',
        login_required(APIKeyListView.as_view()),
        name="api_keys_keys"
    ),
    url(
        r'^(?P<pk>\d+)/delete',
        login_required(APIKeyDeleteView.as_view()),
        name="api_keys_delete_key"
    )
]
