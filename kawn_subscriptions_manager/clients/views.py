from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView

from kawn_subscriptions_manager.decorators import supervisor_only, sales_only
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
        user_role = self.request.user.type
        if user_role == "SALES":
            return Client.objects.filter(user_id=userid).order_by('id')
        else:
            return Client.objects.all().order_by('user_id')

list_client= ListClient.as_view()


@method_decorator([login_required, sales_only], name='dispatch')
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


@method_decorator([login_required, sales_only], name='dispatch')
class UpdateClient(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Client
    fields = ['name','business_name']
    success_message = _("Client successfully updated")
    template_name = 'clients/add_client.html'
    success_url = reverse_lazy('clients:list_client')

update_client = UpdateClient.as_view()


@method_decorator([login_required, sales_only], name='dispatch')
class DeleteClient(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Client
    context_object_name = 'client'
    success_url = reverse_lazy('clients:list_client')
    success_message = _("Client successfully deleted")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(DeleteClient, self).delete(request, *args, **kwargs)

delete_client = DeleteClient.as_view()


@login_required()
@sales_only
def deactivate_client(request, id):
    client = Client.objects.get(pk=id)
    client.is_active = False
    client.save()
    messages.success(request, "Client has been deactivated successfully!")
    return redirect('clients:list_client')


@login_required()
@sales_only
def activate_client(request, id):
    client = Client.objects.get(pk=id)
    client.is_active = True
    client.save()
    messages.success(request, "Client has been activated successfully!")
    return redirect('clients:list_client')