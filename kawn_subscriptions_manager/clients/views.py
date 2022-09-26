from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView

from kawn_subscriptions_manager.users.models import User
from kawn_subscriptions_manager.clients.models import Client
from .forms import ClientAddForm

#Create your views here.
class ListClient(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'clients/list_client.html'
    # paginate_by = 2

    def get_queryset(self):
        userid = self.request.user.id
        return Client.objects.filter(user_id=userid).order_by('id')

list_client= ListClient.as_view()


class AddClient(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Client
    fields = ['name','business_name']
    success_message = _("Client successfully added")
    template_name = 'clients/add_client.html'

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        client = form.save()
        client.user_id = User.objects.get(pk=self.request.user.id)
        client.save()
        return redirect('clients:list_client')

add_client = AddClient.as_view()


class DeleteClient(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Client
    context_object_name = 'client'
    success_url = reverse_lazy('clients:list_client')
    success_message = _("Client successfully deleted")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(DeleteClient, self).delete(request, *args, **kwargs)

delete_client = DeleteClient.as_view()