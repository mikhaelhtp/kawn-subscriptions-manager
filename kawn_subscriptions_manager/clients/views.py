from http import client
from urllib import request
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from view_breadcrumbs import ListBreadcrumbMixin, BaseBreadcrumbMixin
from django_tables2 import SingleTableMixin
from django_filters.views import FilterView
from django_tables2.export.views import ExportMixin

from kawn_subscriptions_manager.decorators import sales_only
from .models import Outlet, Client, Province, City
from kawn_subscriptions_manager.users.models import User
from kawn_subscriptions_manager.api import (
    api_province,
    api_city,
)
from .forms import (
    OutletForm,
    ClientForm,
    OutletClientForm,
    ClientFormForSupervisor,
)
from .filters import OutletFilter, ClientFilter


# CLIENT
class ListClient(
    ListBreadcrumbMixin, ListView, SingleTableMixin, ExportMixin, FilterView
):
    model = Client

    def get_queryset(self):
        user_id = self.request.user.id
        user_role = self.request.user.type
        if user_role == "SALES":
            return Client.objects.filter(user_id=user_id).order_by("-id")
        else:
            return Client.objects.all().order_by("-id")

    def get_context_data(self, object_list=None):
        client = ClientFilter(self.request.GET, queryset=self.get_queryset())
        queryset = object_list if object_list is not None else client.qs
        export_formats = ("csv", "tsv", "xlsx", "json")
        context = {
            "myFilter": client,
            "object_list": queryset,
            "export_formats": export_formats,
        }
        return context

    def get_template_names(self):
        if self.request.user.type == "SALES":
            return ["clients/sales/list_client.html"]
        else:
            return ["clients/list_client.html"]


class AddClient(BaseBreadcrumbMixin, CreateView):
    model = Client
    template_name = "clients/form_client.html"
    crumbs = [
        ("Client", reverse_lazy("clients:list_client")),
        ("Add Client", reverse_lazy("clients:add_client")),
    ]

    def get_form_class(self):
        if self.request.user.type == "SALES":
            return ClientForm
        else:
            return ClientFormForSupervisor

    def form_valid(self, form):
        messages.success(self.request, "Client successfully added")
        client = form.save(commit=False)
        if self.request.user.type == "SALES":
            client.user_id = self.request.user.id
        client.save()

        return redirect("clients:list_client")


class UpdateClient(SuccessMessageMixin, BaseBreadcrumbMixin, UpdateView):
    model = Client
    template_name = "clients/form_client.html"
    success_url = reverse_lazy("clients:list_client")
    success_message = "Client successfully updated!"
    crumbs = [
        ("Client", reverse_lazy("clients:list_client")),
        ("Update Client", reverse_lazy("clients:update_client")),
    ]

    def get_form_class(self):
        if self.request.user.type == "SALES":
            return ClientForm
        else:
            return ClientFormForSupervisor


class DeleteClient(SuccessMessageMixin, BaseBreadcrumbMixin, DeleteView):
    model = Client
    crumbs = [("Delete Client", reverse_lazy("clients:delete_client"))]
    success_url = reverse_lazy("clients:list_client")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Client successfully deleted!")
        return super(DeleteClient, self).delete(request, *args, **kwargs)


class ListOutletClient(ListBreadcrumbMixin, ListView):
    model = Outlet

    def get_context_data(self, object_list=None):
        queryset = (
            object_list
            if object_list is not None
            else Outlet.objects.filter(client_id=self.kwargs["pk"]).order_by("-id")
        )
        context = {
            "object_list": queryset,
            "name": Client.objects.filter(id=self.kwargs["pk"])[0],
            "pk": self.kwargs["pk"],
        }
        return context

    def get_template_names(self):
        if self.request.user.type == "SALES":
            return ["clients/sales/list_outlet_client.html"]
        else:
            return ["clients/list_outlet_client.html"]


class AddClientOutlet(CreateView):
    model = Outlet
    form_class = OutletClientForm
    template_name = "clients/sales/form_outlet.html"
    success_message = _("Outlet successfully added")

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        top = Outlet.objects.order_by("-id")[0]
        outlet = form.save(commit=False)
        outlet.client_id = self.kwargs["pk"]
        outlet.province_read = dict(form.fields["province"].choices)[
            int(self.request.POST.get("province"))
        ]
        outlet.city_read = dict(form.fields["city"].choices)[
            int(self.request.POST.get("city"))
        ]
        outlet.id = top.id + 1
        outlet.save()
        return redirect("clients:list_outlet_client", pk=self.kwargs["pk"])


class UpdateOutletClient(UpdateView):
    model = Outlet
    form_class = OutletClientForm
    template_name = "clients/sales/form_outlet.html"

    def form_valid(self, form):
        messages.success(self.request, "Outlet successfully added")
        outlet_id = Outlet.objects.get(id=self.kwargs["pk"])
        outlet = form.save(commit=False)
        outlet.province_read = dict(form.fields["province"].choices)[
            int(self.request.POST.get("province"))
        ]
        outlet.city_read = dict(form.fields["city"].choices)[
            int(self.request.POST.get("city"))
        ]
        outlet.save()
        return redirect("clients:list_outlet_client", pk=outlet_id.client_id)


class ListOutlet(
    ListBreadcrumbMixin, ListView, SingleTableMixin, ExportMixin, FilterView
):
    model = Outlet
    exclude_columns = (
        "id",
        "display_name",
        "subscription_plan_read",
        "postal_code",
        "outlet_code",
        "outlet_image",
        "is_expired",
        "transaction_code_prefix",
        "archieved",
        "deleted",
        "taxes",
        "gratuity",
        "enable_dashboard",
        "branch_id",
        "device_users",
        "created",
        "modified",
        "province",
        "city",
    )

    def get_queryset(self):
        user_id = self.request.user.id
        client_id = Client.objects.filter(user_id=user_id).values_list("id")
        if self.request.user.type == "SALES":
            return Outlet.objects.filter(client_id__in=client_id).order_by("-id")
        else:
            return Outlet.objects.all().order_by("-id")

    def get_context_data(self, object_list=None):
        outlets = OutletFilter(self.request.GET, queryset=self.get_queryset())
        queryset = object_list if object_list is not None else outlets.qs
        export_formats = ("csv", "tsv", "xlsx", "json")
        context = {
            "myFilter": outlets,
            "object_list": queryset,
            "export_formats": export_formats,
        }
        return context

    def get_template_names(self):
        if self.request.user.type == "SALES":
            return ["clients/sales/list_outlet.html"]
        else:
            return ["clients/list_outlet.html"]


class AddOutlet(BaseBreadcrumbMixin, CreateView):
    model = Outlet
    # form_class = OutletForm
    template_name = "clients/form_outlet.html"
    crumbs = [
        ("Outlet", reverse_lazy("clients:list_outlet")),
        ("Add Outlet", reverse_lazy("clients:add_outlet")),
    ]

    def get_form(self):
        if self.request.method == "POST":
            return OutletForm(data=self.request.POST, user=self.request.user)
        else:
            return OutletForm(user=self.request.user)

    # def get_form_class(self):
    #     return OutletForm(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Outlet successfully added")
        top = Outlet.objects.order_by("-id")[0]
        outlet = form.save(commit=False)
        outlet.province_read = dict(form.fields["province"].choices)[
            int(self.request.POST.get("province"))
        ]
        outlet.city_read = dict(form.fields["city"].choices)[
            int(self.request.POST.get("city"))
        ]
        outlet.id = top.id + 1
        outlet.save()
        return redirect("clients:list_outlet")


class UpdateOutlet(BaseBreadcrumbMixin, UpdateView):
    model = Outlet
    template_name = "clients/form_outlet.html"
    form_class = OutletForm
    # success_url = reverse_lazy("clients:list_outlet")
    crumbs = [
        ("Outlet", reverse_lazy("clients:list_outlet")),
        ("Update Outlet", reverse_lazy("clients:update_outlet")),
    ]

    # def get_form(self):
    #     if self.request.method == "POST":
    #         return OutletForm(data=self.request.POST, user=self.request.user)
    #     else:
    #         return OutletForm(user=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"user": self.request.user})

        return kwargs

    def form_valid(self, form):
        messages.success(self.request, "Outlet successfully updated")
        outlet = form.save(commit=False)
        outlet.province_read = dict(form.fields["province"].choices)[
            int(self.request.POST.get("province"))
        ]
        outlet.city_read = dict(form.fields["city"].choices)[
            int(self.request.POST.get("city"))
        ]
        outlet.save()
        return redirect("clients:list_outlet")


class DeleteOutlet(DeleteView):
    model = Outlet

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Outlet successfully deleted!")
        return super(DeleteOutlet, self).delete(request, *args, **kwargs)

    def get_success_url(self):
        return self.request.META.get("HTTP_REFERER")


def load_cities(request):
    province_id = request.GET.get("province")
    cities = City.objects.filter(province_id=province_id).order_by("name")
    return render(
        request, "clients/city_dropdown_list_options.html", {"cities": cities}
    )
