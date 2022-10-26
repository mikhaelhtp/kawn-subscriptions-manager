from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.generic import UpdateView, CreateView, ListView, DeleteView
from django_tables2 import SingleTableMixin
from django_filters.views import FilterView
from django_tables2.export.views import ExportMixin

from .models import Subscription, SubscriptionPlan
from .forms import AddSubscriptionForm
from .tables import SubscriptionTable
from kawn_subscriptions_manager.decorators import allowed_users, sales_only
from kawn_subscriptions_manager.clients.models import Outlet
from kawn_subscriptions_manager.api import api_subscription_plans, api_subscriptions
from kawn_subscriptions_manager.filters import (
    SubscriptionPlanFilter,
    SubscriptionFilter,
)


class ListSubscriptionPlan(ListView, SingleTableMixin, ExportMixin, FilterView):
    model = SubscriptionPlan
    filterset_class = SubscriptionPlanFilter
    queryset = SubscriptionPlan.objects.all().order_by("id")
    paginate_by = 10

    def get_context_data(self, object_list=None):
        subscription_plan_filter = SubscriptionPlanFilter(
            self.request.GET, queryset=self.queryset
        )
        queryset = (
            object_list if object_list is not None else subscription_plan_filter.qs
        )
        page_size = self.get_paginate_by(self.queryset)
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset, page_size
        )
        context = {
            "subscription_plan_filter": subscription_plan_filter,
            "object_list": queryset,
            "paginator": paginator,
            "page_obj": page,
            "is_paginated": is_paginated,
        }
        return context
        

    def get_template_names(self):
        if self.request.user.type == "SALES":
            return [
                "subscriptions/subscription_plans/sales/list_subscription_plan.html"
            ]
        else:
            return ["subscriptions/subscription_plans/list_subscription_plan.html"]


@method_decorator([allowed_users(["ADMIN", "SUPERVISOR"])], name="dispatch")
class AddSubscriptionPlan(SuccessMessageMixin, CreateView):
    model = SubscriptionPlan
    fields = [
        "name",
        "price",
        "description",
        "trial_unit",
        "trial_period",
        "recurrence_unit",
        "recurrence_period",
    ]
    template_name = "subscriptions/subscription_plans/form_subscription_plan.html"
    success_url = reverse_lazy("subscriptions:list_subscription_plan")
    success_message = "Subscription plans successfully added!"


@method_decorator([allowed_users(["ADMIN", "SUPERVISOR"])], name="dispatch")
class UpdateSubscriptionPlan(SuccessMessageMixin, UpdateView):
    model = SubscriptionPlan
    fields = [
        "name",
        "price",
        "description",
        "trial_unit",
        "trial_period",
        "recurrence_unit",
        "recurrence_period",
    ]
    template_name = "subscriptions/subscription_plans/form_subscription_plan.html"
    success_url = reverse_lazy("subscriptions:list_subscription_plan")
    success_message = "Subscription plans successfully updated!"


@method_decorator([allowed_users(["ADMIN", "SUPERVISOR"])], name="dispatch")
class DeleteSubscriptionPlan(DeleteView):
    model = SubscriptionPlan
    success_url = reverse_lazy("subscriptions:list_subscription_plan")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Subscription plans successfully delated!")
        return super(DeleteSubscriptionPlan, self).delete(request, *args, **kwargs)


@allowed_users(allowed_roles=["ADMIN", "SUPERVISOR"])
def deactivate_subscription_plan(request, id):
    subscriptionplan = SubscriptionPlan.objects.get(pk=id)
    subscriptionplan.is_active = False
    subscriptionplan.save()
    messages.success(request, "Subscription plans has been successfully deactivated!")
    return redirect("subscriptions:list_subscription_plan")


@allowed_users(allowed_roles=["ADMIN", "SUPERVISOR"])
def activate_subscription_plan(request, id):
    subscriptionplan = SubscriptionPlan.objects.get(pk=id)
    subscriptionplan.is_active = True
    subscriptionplan.save()
    messages.success(request, "Subscription plans has been successfully activated!")
    return redirect("subscriptions:list_subscription_plan")


class ListSubscription(ListView, SingleTableMixin, ExportMixin, FilterView):
    model = Subscription
    filterset_class = SubscriptionFilter
    # table_class = SubscriptionTable
    paginate_by = 10

    # def get_queryset(self):
    #     userid = self.request.user.id
    #     user_role = self.request.user.type
    #     if user_role == "SALES":
    #         subscription = Subscription.objects.values_list("outlet_id")
    #         outlet = Outlet.objects.filter(
    #             id__in=subscription, user_id=self.request.user.id
    #         ).values_list("id") 
    #         return Subscription.objects.filter(outlet_id__in=outlet).order_by("id")
    #     else:
    #         return Subscription.objects.all().order_by("id")

    def get_context_data(self, object_list=None):
        subscription_filter = SubscriptionFilter(
            self.request.GET, queryset=self.get_queryset()
        )
        queryset = object_list if object_list is not None else subscription_filter.qs
        export_formats = ("csv", "tsv", "xlsx", "json")
        page_size = self.paginate_by
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset, page_size
        )
        context = {
            "subscription_filter": subscription_filter,
            "object_list": queryset,
            "export_formats": export_formats,
            "paginator": paginator,
            "page_obj": page,
            "is_paginated": is_paginated,
        }
        return context

    def get_template_names(self):
        if self.request.user.type == "SALES":
            return ["subscriptions/sales/list_subscription.html"]
        else:
            return ["subscriptions/list_subscription.html"]
    
    def get_table_kwargs(self):
        return {"template_name": "subscriptions/sales/list_subscription.html"}

    now = timezone.now()
    Subscription.objects.filter(expires__lte=now).update(active=False)


@method_decorator([sales_only], name="dispatch")
class AddSubscription(CreateView):
    model = Subscription
    template_name = "subscriptions/form_subscription.html"

    def get_form(self):
        if self.request.method == "POST":
            return AddSubscriptionForm(data=self.request.POST, user=self.request.user)
        else:
            return AddSubscriptionForm(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Subscriptions successfully added!")
        top = Subscription.objects.order_by("-id")[0]
        subscription = form.save(commit=False)
        subscription.id = top.id+1
        subscription.save()
        return redirect("subscriptions:list_subscription")


class ActivateSubscription(SuccessMessageMixin, UpdateView):
    model = Subscription
    success_message = _("Subscription successfully updated!")
    fields = ["expires"]
    template_name = "subscriptions/form_subscription.html"
    success_url = reverse_lazy("subscriptions:list_subscription")

    def form_valid(self, form):
        subscription = form.save()
        now = timezone.now()
        if form.cleaned_data["expires"] > now:
            subscription.active = True
            subscription.save()
        else:
            subscription.active = False
            subscription.save()
        return super().form_valid(form)


def deactivate_subscription(request, id):
    subscription = Subscription.objects.get(pk=id)
    subscription.active = False
    subscription.save()
    messages.success(request, "Subscriptions has been deactivated successfully!")
    return redirect("subscriptions:list_subscription")
