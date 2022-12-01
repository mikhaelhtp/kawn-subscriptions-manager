from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    UpdateView,
    CreateView,
    ListView,
    DeleteView,
    DetailView,
)
from django_tables2 import SingleTableMixin
from django_tables2.export.views import ExportMixin

from json import dumps
import simplejson as json
from view_breadcrumbs import ListBreadcrumbMixin, BaseBreadcrumbMixin

from .models import (
    SubscriptionPlan,
    Subscription,
    Billing,
    OrderPayment,
    SubscriptionDetail,
)
from .forms import (
    AddSubscriptionMultiForm,
    ActivateSubscriptionMultiForm,
)
from .filters import (
    SubscriptionPlanFilter,
    SubscriptionFilter,
    ActivityFilter,
)
from kawn_subscriptions_manager.clients.models import Client, Outlet
from kawn_subscriptions_manager.decorators import allowed_users, sales_only


class ListSubscriptionPlan(
    ListBreadcrumbMixin, ListView, SingleTableMixin, ExportMixin
):
    model = SubscriptionPlan
    filterset_class = SubscriptionPlanFilter
    queryset = SubscriptionPlan.objects.all().order_by("id")

    def get_context_data(self, object_list=None):
        subscription_plan_filter = SubscriptionPlanFilter(
            self.request.GET, queryset=self.queryset
        )
        queryset = (
            object_list if object_list is not None else subscription_plan_filter.qs
        )
        context = {
            "subscription_plan_filter": subscription_plan_filter,
            "object_list": queryset,
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
class AddSubscriptionPlan(SuccessMessageMixin, BaseBreadcrumbMixin, CreateView):
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
    crumbs = [
        ("Subscription Plans", reverse_lazy("subscriptions:list_subscription_plan")),
        ("Add Subscription Plans", reverse_lazy("subscriptions:add_subscription_plan")),
    ]
    template_name = "subscriptions/subscription_plans/form_subscription_plan.html"

    def form_valid(self, form):
        messages.success(self.request, "Subscription plans successfully added!")
        subscription_plan = form.save(commit=False)
        
        if SubscriptionPlan.objects.all().exists():
            top = SubscriptionPlan.objects.order_by("-id")[0]
            subscription_plan.id = top.id + 1
        subscription_plan.save()
        return redirect("subscriptions:list_subscription_plan")


@method_decorator([allowed_users(["ADMIN", "SUPERVISOR"])], name="dispatch")
class UpdateSubscriptionPlan(SuccessMessageMixin, BaseBreadcrumbMixin, UpdateView):
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
    crumbs = [
        ("Subscription Plans", reverse_lazy("subscriptions:list_subscription_plan")),
        (
            "Update Subscription Plans",
            reverse_lazy("subscriptions:update_subscription_plan"),
        ),
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
def deactivate_subscription_plan(request, slug):
    subscriptionplan = SubscriptionPlan.objects.get(slug=slug)
    subscriptionplan.is_active = False
    subscriptionplan.save()
    messages.success(request, "Subscription plans has been successfully deactivated!")
    return redirect("subscriptions:list_subscription_plan")


@allowed_users(allowed_roles=["ADMIN", "SUPERVISOR"])
def activate_subscription_plan(request, slug):
    subscriptionplan = SubscriptionPlan.objects.get(slug=slug)
    subscriptionplan.is_active = True
    subscriptionplan.save()
    messages.success(request, "Subscription plans has been successfully activated!")
    return redirect("subscriptions:list_subscription_plan")


class ListSubscription(ListBreadcrumbMixin, ListView, SingleTableMixin, ExportMixin):
    model = Subscription
    filterset_class = SubscriptionFilter

    def get_context_data(self, object_list=None):
        subscription_filter = SubscriptionFilter(
            self.request.GET, queryset=self.get_queryset()
        )
        queryset = object_list if object_list is not None else subscription_filter.qs
        export_formats = ("csv", "tsv", "xlsx", "json")
        context = {
            "subscription_filter": subscription_filter,
            "object_list": queryset,
            "export_formats": export_formats,
        }
        return context

    def get_queryset(self):
        user_id = self.request.user.id
        client = Client.objects.filter(user_id=user_id).values_list("id")
        outlet = Outlet.objects.filter(client_id__in=client)
        user_role = self.request.user.type
        if user_role == "SALES":
            return Subscription.objects.filter(outlet_id__in=outlet).order_by("-id")
        else:
            return Subscription.objects.all().order_by("-id")

    def get_template_names(self):
        if self.request.user.type == "SALES":
            return ["subscriptions/sales/list_subscription.html"]
        else:
            return ["subscriptions/list_subscription.html"]

    def __init__(self):
        now = timezone.now()
        Subscription.objects.filter(expires__lte=now).update(active=False)


@method_decorator([allowed_users(["ADMIN", "SUPERVISOR"])], name="dispatch")
class DetailSubscription(DetailView):
    model = Subscription
    template_name = "subscriptions/detail_subscription.html"


@method_decorator([sales_only], name="dispatch")
class AddSubscription(BaseBreadcrumbMixin, CreateView):
    model = Subscription
    form_class = AddSubscriptionMultiForm
    crumbs = [
        ("Subscription", reverse_lazy("subscriptions:list_subscription")),
        ("Add Subscription", reverse_lazy("subscriptions:add_subscription")),
    ]
    template_name = "subscriptions/sales/form_subscription.html"

    def get_form_kwargs(self):
        kwargs = super(AddSubscription, self).get_form_kwargs()
        kwargs["request"] = self.request

        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["subscriptionplan"] = json.dumps(
            list(SubscriptionPlan.objects.values("id", "price", "recurrence_period"))
        )
        return context

    def form_valid(self, form):
        messages.success(self.request, "Subscriptions successfully added!")
        name_type = dict(
            {"name": self.request.user.name, "type": self.request.user.type}
        )
        order_payment = form["add_order_payment_form"].save(commit=False)
        order_payment.save()
        top_order_payment = OrderPayment.objects.order_by("-id")[0]
        subscription_detail = SubscriptionDetail(
            outlet=form["add_subscription_form"].cleaned_data["outlet"].id,
            current_plan=form["add_subscription_form"]
            .cleaned_data["subscriptionplan"]
            .id,
            choosen_plan=form["add_subscription_form"]
            .cleaned_data["subscriptionplan"]
            .id,
        )
        subscription_detail.save()
        top_subscription_detail = SubscriptionDetail.objects.order_by("-id")[0]
        billing = form["add_billing_form"].save(commit=False)
        billing.orderpayment_id = top_order_payment.id
        billing.subscriptiondetail_id = top_subscription_detail.id
        billing.save()
        top_billing = Billing.objects.order_by("-id")[0]
        subscription = form["add_subscription_form"].save(commit=False)
        subscription.billing_id = top_billing.id
        subscription.created_by = name_type
        if Subscription.objects.all().exists():
            top = Subscription.objects.order_by("-id")[0]
            subscription.id = top.id + 1
        subscription.save()
        return redirect("subscriptions:list_subscription")


@method_decorator([allowed_users(["SALES"])], name="dispatch")
class ActivateSubscription(BaseBreadcrumbMixin, UpdateView):
    model = Subscription
    form_class = ActivateSubscriptionMultiForm
    template_name = "subscriptions/sales/form_subscription.html"
    crumbs = [
        ("Subscription", reverse_lazy("subscriptions:list_subscription")),
        ("Activate Subscription", reverse_lazy("subscriptions:add_subscription")),
    ]

    def get_form_kwargs(self):
        outlet = (Subscription.objects.get(slug=self.kwargs["slug"])).outlet
        kwargs = super(ActivateSubscription, self).get_form_kwargs()
        kwargs["outlet_id"] = outlet
        print(outlet)
        kwargs.update(
            instance={
                "activate_subscription_form": self.object,
                "activate_billing_form": self.object.billing,
            }
        )

        return kwargs

    def form_valid(self, form):
        messages.success(self.request, "Subscriptions successfully added!")
        name_type = dict(
            {"name": self.request.user.name, "type": self.request.user.type}
        )
        billing_id = (Subscription.objects.get(slug=self.kwargs["slug"])).billing
        order_payment_id = (Billing.objects.get(id=billing_id.id)).orderpayment
        order_payment = OrderPayment.objects.get(pk=order_payment_id.id)
        order_payment.payment_type = form["activate_order_payment_form"].cleaned_data[
            "payment_type"
        ]
        order_payment.amount = form["activate_order_payment_form"].cleaned_data[
            "amount"
        ]
        order_payment.save()
        subscription_detail_id = (
            Billing.objects.get(id=billing_id.id)
        ).subscriptiondetail
        subscription_detail = SubscriptionDetail.objects.get(
            pk=subscription_detail_id.id
        )
        subscription_detail.current_plan = (
            form["activate_subscription_form"].cleaned_data["subscriptionplan"].id
        )
        subscription_detail.choosen_plan = (
            form["activate_subscription_form"].cleaned_data["subscriptionplan"].id
        )
        subscription_detail.save()
        billing = form["activate_billing_form"].save(commit=False)
        billing.save()
        subscription = form["activate_subscription_form"].save(commit=False)
        subscription.is_approved = ""
        subscription.modified_by = name_type
        subscription.save()

        return redirect("subscriptions:list_subscription")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["subscriptionplan"] = json.dumps(
            list(SubscriptionPlan.objects.values("id", "price", "recurrence_period"))
        )
        return context


@allowed_users(allowed_roles=["SALES"])
def deactivate_subscription(request, slug):
    subscription = Subscription.objects.get(slug=slug)
    name_type = dict({"name": request.user.name, "type": request.user.type})
    subscription.active = True
    subscription.modified_by = name_type
    subscription.is_approved = ""
    subscription.save()
    messages.success(
        request,
        mark_safe(
            "Subscription deactivation request has been successful! <br/>Please wait for the deactivation process."
        ),
    )
    return redirect("subscriptions:list_subscription")


@method_decorator([allowed_users(["ADMIN", "SUPERVISOR"])], name="dispatch")
class ListApprovalRequest(ListView):
    model = Subscription
    queryset = Subscription.objects.filter(is_approved=None)

    def get_template_names(self):
        return "subscriptions/list_approval.html"


@method_decorator([allowed_users(["ADMIN", "SUPERVISOR"])], name="dispatch")
class DetailApprovalRequest(DetailView):
    model = Subscription
    template_name = "subscriptions/detail_approval.html"


@allowed_users(allowed_roles=["ADMIN", "SUPERVISOR"])
def accept_subscription(request, slug):
    subscription = Subscription.objects.get(slug=slug)
    name_type = dict({"name": request.user.name, "type": request.user.type})

    if subscription.active is not True:
        subscription.active = True
        subscription.save()
    else:
        subscription.active = False
        subscription.save()
    subscription.is_approved = True
    subscription.modified_by = name_type
    subscription.save()
    messages.success(request, "Subscriptions have been approved!")
    return redirect("subscriptions:list_approval")


@allowed_users(allowed_roles=["ADMIN", "SUPERVISOR"])
def decline_subscription(request, slug):
    subscription = Subscription.objects.get(slug=slug)
    name_type = dict({"name": request.user.name, "type": request.user.type})
    if subscription.active is not True:
        subscription.active = False
        subscription.save()
    elif subscription.active is not False:
        subscription.active == True
        subscription.save()
    subscription.is_approved = False
    subscription.modified_by = name_type
    subscription.save()
    messages.success(request, "Subscriptions have been rejected!")
    return redirect("subscriptions:list_approval")


@method_decorator([allowed_users(["ADMIN", "SUPERVISOR"])], name="dispatch")
class SubscriptionLogs(ListView):
    model = Subscription
    queryset = Subscription.objects.all().order_by("-modified")

    def get_template_names(self):
        return "subscriptions/subscription_logs.html"


class ActivityLogsCreated(ListView):
    model = Subscription
    template_name = "subscriptions/activity_logs_created.html"
    paginate_by = 5
    
    def get_queryset(self):
        return Subscription.objects.filter(created_by__isnull=False).order_by("-created")

    def get_context_data(self, object_list=None):
        activity_logs = ActivityFilter(self.request.GET, queryset=self.get_queryset())
        queryset = object_list if object_list is not None else activity_logs.qs
        page_size = self.paginate_by
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset, page_size
        )
        context = {
            "myFilter": activity_logs,
            "object_list": queryset,
            "paginator": paginator,
            "page_obj": page,
            "is_paginated": is_paginated,
        }
        return context


class ActivityLogsModified(ListView):
    model = Subscription
    template_name = "subscriptions/activity_logs_modified.html"
    paginate_by = 5
    
    def get_queryset(self):
        return Subscription.objects.filter(modified_by__isnull=False).order_by("-modified")

    def get_context_data(self, object_list=None):
        activity_logs = ActivityFilter(self.request.GET, queryset=self.get_queryset())
        queryset = object_list if object_list is not None else activity_logs.qs
        page_size = self.paginate_by
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset, page_size
        )
        context = {
            "myFilter": activity_logs,
            "object_list": queryset,
            "paginator": paginator,
            "page_obj": page,
            "is_paginated": is_paginated,
        }
        return context