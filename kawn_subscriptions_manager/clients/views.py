from http import client
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
    api_outlet,
    api_outlet1,
    api_province,
    api_city,
)
from .forms import AddOutletForm, AddClientForm, UpdateClientForm, AddClientOutletForm
from .filters import OutletFilter, ClientFilter


# CLIENT
class ListClient(
    ListBreadcrumbMixin, ListView, SingleTableMixin, ExportMixin, FilterView
):
    model = Outlet
    paginate_by = 10

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
        page_size = self.paginate_by
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset, page_size
        )
        context = {
            "myFilter": client,
            "object_list": queryset,
            "export_formats": export_formats,
            "paginator": paginator,
            "page_obj": page,
            "is_paginated": is_paginated,
        }
        return context

    def get_template_names(self):
        if self.request.user.type == "SALES":
            return ["clients/sales/list_client.html"]
        else:
            return ["clients/list_client.html"]


@method_decorator([sales_only], name="dispatch")
class AddClient(BaseBreadcrumbMixin, CreateView):
    model = Client
    form_class = AddClientForm
    crumbs = [
        ("Client", reverse_lazy("clients:list_client")),
        ("Add Client", reverse_lazy("clients:add_client")),
    ]
    template_name = "clients/sales/form_client.html"

    def form_valid(self, form):
        messages.success(self.request, "Client successfully added")
        client = form.save(commit=False)
        client.user_id = self.request.user.id
        client.save()
        return redirect("clients:list_client")


class UpdateClient(SuccessMessageMixin, BaseBreadcrumbMixin, UpdateView):
    model = Client
    form_class = UpdateClientForm
    crumbs = [
        ("Client", reverse_lazy("clients:list_client")),
        ("Update Client", reverse_lazy("clients:update_client")),
    ]
    template_name = "clients/sales/form_client.html"
    success_url = reverse_lazy("clients:list_client")
    success_message = "Client successfully updated!"


@method_decorator([sales_only], name="dispatch")
class DeleteClient(SuccessMessageMixin, BaseBreadcrumbMixin, DeleteView):
    model = Client
    crumbs = [("Delete Client", reverse_lazy("clients:delete_client"))]
    success_url = reverse_lazy("clients:list_client")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Client successfully delated!")
        return super(DeleteClient, self).delete(request, *args, **kwargs)


class ListOutletClient(ListBreadcrumbMixin, ListView):
    model = Outlet
    paginate_by = 10

    def get_context_data(self, object_list=None):
        queryset = (
            object_list
            if object_list is not None
            else Outlet.objects.filter(client_id=self.kwargs["pk"]).order_by("-id")
        )
        page_size = self.paginate_by
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset, page_size
        )
        context = {
            "object_list": queryset,
            "name": Client.objects.filter(id=self.kwargs["pk"])[0],
            "pk": self.kwargs["pk"],
            "paginator": paginator,
            "page_obj": page,
            "is_paginated": is_paginated,
        }
        return context

    def get_template_names(self):
        if self.request.user.type == "SALES":
            return ["clients/sales/list_outlet_client.html"]
        else:
            return ["clients/list_outlet_client.html"]


@method_decorator([sales_only], name="dispatch")
class AddClientOutlet(CreateView):
    form_class = AddClientOutletForm
    template_name = "clients/sales/form_outlet.html"
    success_message = _("Outlet successfully added")

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        client = form.save() 
        client.client_id = self.kwargs["pk"]
        client.save()
        return redirect("clients:list_outlet_client", pk=self.kwargs["pk"])


def DeleteClientOutlet(request, pk):
    Outlet.objects.filter(id=pk).update(client_id="")
    messages.success(request, "Outlet successfully deleted")
    return redirect(request.META.get("HTTP_REFERER"))


class ListOutlet(
    ListBreadcrumbMixin, ListView, SingleTableMixin, ExportMixin, FilterView
):
    model = Outlet
    queryset = Outlet.objects.all().order_by("-id")
    paginate_by = 10
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

    def get_context_data(self, object_list=None):
        outlets = OutletFilter(self.request.GET, queryset=self.queryset)
        queryset = object_list if object_list is not None else outlets.qs
        export_formats = ("csv", "tsv", "xlsx", "json")
        page_size = self.paginate_by
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset, page_size
        )
        context = {
            "myFilter": outlets,
            "object_list": queryset,
            "export_formats": export_formats,
            "paginator": paginator,
            "page_obj": page,
            "is_paginated": is_paginated,
        }
        return context

    def get_template_names(self):
        if self.request.user.type == "SALES":
            return ["clients/sales/list_outlet.html"]
        else:
            return ["clients/list_outlet.html"]


class AddOutlet(BaseBreadcrumbMixin, CreateView):
    model = Outlet
    form_class = AddOutletForm
    crumbs = [
        ("Outlet", reverse_lazy("clients:list_outlet")),
        ("Add Outlet", reverse_lazy("clients:add_outlet")),
    ]
    success_message = _("Outlet successfully added")
    template_name = "clients/form_outlet.html"

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
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


class UpdateOutlet(SuccessMessageMixin, BaseBreadcrumbMixin, UpdateView):
    model = Outlet
    form_class = AddOutletForm
    crumbs = [
        ("Outlet", reverse_lazy("clients:list_outlet")),
        ("Update Outlet", reverse_lazy("clients:update_outlet")),
    ]
    success_message = _("Outlet successfully updated")
    template_name = "clients/form_outlet.html"
    success_url = reverse_lazy("clients:list_outlet")

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        outlet = form.save(commit=False)
        outlet.province_read = dict(form.fields["province"].choices)[
            int(self.request.POST.get("province"))
        ]
        outlet.city_read = dict(form.fields["city"].choices)[
            int(self.request.POST.get("city"))
        ]
        outlet.save()
        return redirect("clients:list_outlet")


def load_cities(request):
    province_id = request.GET.get("province")
    cities = City.objects.filter(province_id=province_id).order_by("name")
    return render(
        request, "clients/city_dropdown_list_options.html", {"cities": cities}
    )
