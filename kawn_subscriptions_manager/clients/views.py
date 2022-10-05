from django.contrib.messages.views import SuccessMessageMixin
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView

from kawn_subscriptions_manager.decorators import sales_only
from kawn_subscriptions_manager.clients.models import Client, Outlet
from kawn_subscriptions_manager.users.models import User


class ListClient(ListView):
    model = Client
    template_name = "clients/list_client.html"
    # paginate_by = 2

    def get_queryset(self):
        userid = self.request.user.id
        user_role = self.request.user.type
        if user_role == "SALES":
            return Client.objects.filter(user_id=userid).order_by("id")
        else:
            return Client.objects.all().order_by("user_id")

    def get_template_names(self):
        if self.request.user.type == "SALES":
            return ["clients/sales/list_client.html"]
        else:
            return ["clients/list_client.html"]


@method_decorator([sales_only], name="dispatch")
class AddClient(CreateView):
    model = Client
    fields = ["name"]
    success_message = _("Client successfully added")
    template_name = "clients/form_client.html"

    def form_valid(self, form):
        messages.success(self.request, "Client successfully added")
        client = form.save()
        client.user_id = User.objects.get(pk=self.request.user.id)
        client.save()
        return redirect("clients:list_client")


class UpdateClient(SuccessMessageMixin, UpdateView):
    model = Client
    fields = ["name"]
    success_message = _("Client successfully updated")
    template_name = "clients/form_client.html"
    success_url = reverse_lazy("clients:list_client")


class DeleteClient(DeleteView):
    model = Client
    context_object_name = "client"
    success_url = reverse_lazy("clients:list_client")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Client successfully deleted")
        return super(DeleteClient, self).delete(request, *args, **kwargs)


def deactivate_client(request, id):
    client = Client.objects.get(pk=id)
    client.is_active = False
    client.save()
    messages.success(request, "Client has been deactivated successfully!")
    return redirect("clients:list_client")


def activate_client(request, id):
    client = Client.objects.get(pk=id)
    client.is_active = True
    client.save()
    messages.success(request, "Client has been activated successfully!")
    return redirect("clients:list_client")


class ListOutlet(ListView):
    model = Outlet
    template_name = "clients/list_outlet_client.html"

    def get_context_data(self):
        context = {
            "object_list": Outlet.objects.filter(client_id=self.kwargs["id"]),
            "id": self.kwargs["id"],
        }
        return context

    def get_template_names(self):
        if self.request.user.type == "SALES":
            return ["clients/sales/list_outlet_client.html"]
        else:
            return ["clients/list_outlet_client.html"]


class AddOutlet(SuccessMessageMixin, CreateView):
    model = Outlet
    fields = ["name"]
    success_message = _("Outlet successfully added")
    template_name = "clients/form_outlet.html"

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        outlet = form.save()
        outlet.client_id = self.kwargs["id"]
        outlet.save()
        return redirect("clients:list_outlet_client", id=self.kwargs["id"])
