from django.contrib.messages.views import SuccessMessageMixin
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django_tables2 import SingleTableMixin
from django_filters.views import FilterView
from django_tables2.export.views import ExportMixin

from kawn_subscriptions_manager.decorators import sales_only
from .models import Outlet, Account
from kawn_subscriptions_manager.users.models import User
from kawn_subscriptions_manager.api import api_outlet, api_outlet1
from .forms import AddOutletForm, AddClientForm, UpdateClientForm, AddClientOutletForm
from .filters import OutletFilter, AccountFilter


#CLIENT
class ListClient(ListView):
    model = Outlet
    paginate_by = 10

    def get_queryset(self):
        user_id = self.request.user.id
        user_role = self.request.user.type
        if user_role == "SALES":
            return Account.objects.filter(user_id=user_id).order_by("-id")
        else:
            return Account.objects.all().order_by("-id")

    def get_context_data(self, object_list=None):
        account = AccountFilter(self.request.GET, queryset=self.get_queryset())
        queryset = object_list if object_list is not None else account.qs
        page_size = self.paginate_by
        paginator, page, queryset, is_paginated = self.paginate_queryset(queryset, page_size)
        context = {
            'myFilter' : account,
            'object_list' : queryset,
            'paginator': paginator,
            'page_obj': page,
            'is_paginated': is_paginated,
        }
        return context

    def get_template_names(self):
        if self.request.user.type == "SALES":
            return ["clients/sales/list_client.html"]
        else:
            return ["clients/list_client.html"]


@method_decorator([sales_only], name="dispatch")
class AddClient(CreateView):
    model = Account
    form_class = AddClientForm
    success_message = _("Client successfully added")
    template_name = "clients/sales/form_client.html"

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        account = form.save(commit=False)
        account.user_id = self.request.user.id
        if form.cleaned_data["brand_name"] == None:
            account.brand_name = "-"
        if form.cleaned_data["social_facebook"] == None:
            account.social_facebook = "-"
        if form.cleaned_data["social_instagram"] == None:
            account.social_instagram = "-"
        if form.cleaned_data["social_twitter"] == None:
            account.social_twitter = "-"
        if form.cleaned_data["website"] == None:
            account.website = "-"
        account.save()
        return redirect("clients:list_client")


class UpdateClient(SuccessMessageMixin, UpdateView):
    model = Account
    form_class = UpdateClientForm
    template_name = "clients/sales/form_client.html"
    success_url = reverse_lazy("clients:list_client")
    success_message = "Client successfully updated!"


@method_decorator([sales_only], name="dispatch")
class DeleteClient(SuccessMessageMixin, DeleteView):
    model = Account
    success_url = reverse_lazy("clients:list_client")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Client successfully delated!")
        return super(DeleteClient, self).delete(request, *args, **kwargs)


#Outlet
class ListOutletClient(ListView):
    model = Outlet
    # paginate_by = 10

    def get_context_data(self):
        context = {
            "object_list": Outlet.objects.filter(account_id=self.kwargs["pk"]),
            "name": Account.objects.filter(id=self.kwargs["pk"])[0],
            "pk": self.kwargs["pk"],
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
        Outlet.objects.filter(id=form.cleaned_data["name"]).update(account_id=self.kwargs["pk"])
        return redirect("clients:list_outlet_client", pk=self.kwargs["pk"])


def DeleteClientOutlet(request, pk):
    Outlet.objects.filter(id=pk).update(account_id="")
    messages.success(request, "Outlet successfully deleted")
    # return redirect("clients:list_outlet_client", pk=2)
    return redirect(request.META.get('HTTP_REFERER'))


class ListOutlet(ListView, SingleTableMixin, ExportMixin, FilterView):
    model = Outlet
    template_name = "clients/list_outlet.html"
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
        paginator, page, queryset, is_paginated = self.paginate_queryset(queryset, page_size)
        context = {
            'myFilter' : outlets,
            'object_list' : queryset,
            "export_formats": export_formats,
            'paginator': paginator,
            'page_obj': page,
            'is_paginated': is_paginated,
        }
        return context
    
    def get_table_kwargs(self):
        return {"template_name": "clients/list_outlet.html"}


class AddOutlet(CreateView):
    model = Outlet
    form_class = AddOutletForm
    success_message = _("Outlet successfully added")
    template_name = "clients/form_outlet.html"

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        top = Outlet.objects.order_by("-id")[0]
        outlet = form.save(commit=False)
        outlet.id = top.id+1
        outlet.save()
        return redirect("clients:list_outlet")


class UpdateOutlet(SuccessMessageMixin, UpdateView):
    model = Outlet
    form_class = AddOutletForm
    success_message = _("Outlet successfully updated")
    template_name = "clients/form_outlet.html"
    success_url = reverse_lazy("clients:list_outlet")


