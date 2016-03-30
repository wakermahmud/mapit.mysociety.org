from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, DeleteView
from django.http import Http404

from .models import APIKey


class APIKeyListView(ListView):
    template_name = 'api_keys/api_key_list.html'
    context_object_name = 'api_keys'
    model = APIKey

    def get_queryset(self):
        return APIKey.objects.filter(user=self.request.user)


class APIKeyDeleteView(DeleteView):
    template_name = 'api_keys/api_key_delete_confirm.html'
    context_object_name = 'api_key'
    model = APIKey
    success_url = reverse_lazy('api_keys_keys')

    def get_object(self, queryset=None):
        """ Hook to ensure api_key is owned by request.user. """
        api_key = super(APIKeyDeleteView, self).get_object()
        if not api_key.user == self.request.user:
            raise Http404
        return api_key
