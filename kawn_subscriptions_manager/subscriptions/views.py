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
    TemplateView,
    DetailView
)
from view_breadcrumbs import ListBreadcrumbMixin, BaseBreadcrumbMixin
from django_tables2 import SingleTableMixin
from django_filters.views import FilterView
from django_tables2.export.views import ExportMixin
from itertools import chain

from json import dumps

from .models import (
    SubscriptionPlan,
    Subscription,
    Billing,
    OrderPayment,
    SubscriptionDetail,
)
from .forms import (
    AddSubscriptionMultiForm,
    ActivateSubscriptionForm,
    ActivateSubscriptionMultiForm,
)
from .filters import (
    SubscriptionPlanFilter,
    SubscriptionFilter,
)
from kawn_subscriptions_manager.clients.models import Client, Outlet
from kawn_subscriptions_manager.users.models import User
from kawn_subscriptions_manager.decorators import allowed_users, sales_only
from kawn_subscriptions_manager.api import (
    api_outlet,
    api_outlet1,
    api_subscription_plans,
    api_subscriptions,
)


class ListSubscriptionPlan(
    ListBreadcrumbMixin, ListView, SingleTableMixin, ExportMixin, FilterView
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
    success_url = reverse_lazy("subscriptions:list_subscription_plan")
    success_message = "Subscription plans successfully added!"


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


class ListSubscription(
    ListBreadcrumbMixin, ListView, SingleTableMixin, ExportMixin, FilterView
):
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

    now = timezone.now()
    Subscription.objects.filter(expires__lte=now).update(active=False)


@method_decorator([sales_only], name="dispatch")
class AddSubscription(BaseBreadcrumbMixin, CreateView):
    model = Subscription
    form_class = AddSubscriptionMultiForm
    crumbs = [
        ("Subscription", reverse_lazy("subscriptions:list_subscription")),
        ("Add Subscription", reverse_lazy("subscriptions:add_subscription")),
    ]
    template_name = "subscriptions/form_subscription.html"

    def get_form_kwargs(self):
        kwargs = super(AddSubscription, self).get_form_kwargs()
        kwargs["request"] = self.request

        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["subscriptionplan"] = dumps(
            list(SubscriptionPlan.objects.values("id", "price"))
        )
        return context

    def form_valid(self, form):
        messages.success(self.request, "Subscriptions successfully added!")
        top = Subscription.objects.order_by("-id")[0]
        name_type = dict(
            {"name": self.request.user.name, "type": self.request.user.type}
        )
        order_payment = form["add_order_payment_form"].save(commit=False)
        order_payment.save()
        top_order_payment = OrderPayment.objects.order_by("-id")[0]
        subscription_detail = SubscriptionDetail(
            outlet = form["add_subscription_form"].cleaned_data["outlet"].id,
            current_plan=form["add_subscription_form"].cleaned_data["subscriptionplan"].id,
            choosen_plan=form["add_subscription_form"].cleaned_data["subscriptionplan"].id,
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
        subscription.id = top.id + 1
        subscription.save()
        return redirect("subscriptions:list_subscription")


@method_decorator([allowed_users(["ADMIN", "SUPERVISOR"])], name="dispatch")
class ActivateSubscription(BaseBreadcrumbMixin, UpdateView):
    model = Subscription
    form_class = ActivateSubscriptionMultiForm
    template_name = "subscriptions/form_subscription.html"
    crumbs = [
        ("Subscription", reverse_lazy("subscriptions:list_subscription")),
        ("Activate Subscription", reverse_lazy("subscriptions:add_subscription")),
    ]
    
    def get_form_kwargs(self):
        outlet = (Subscription.objects.get(id=self.kwargs["pk"])).outlet
        kwargs = super(ActivateSubscription, self).get_form_kwargs()
        kwargs["outlet_id"] = outlet
        print(outlet)
        kwargs.update(instance={
            'activate_subscription_form': self.object,
            'activate_billing_form': self.object.billing,
        })

        return kwargs
    
    def form_valid(self, form):
        messages.success(self.request, "Subscriptions successfully added!")
        name_type = dict(
            {"name": self.request.user.name, "type": self.request.user.type}
        )
        billing_id = (Subscription.objects.get(id=self.kwargs["pk"])).billing
        order_payment_id = (Billing.objects.get(id=billing_id.id)).orderpayment
        order_payment = OrderPayment.objects.get(pk=order_payment_id.id)
        order_payment.payment_type=form["activate_order_payment_form"].cleaned_data["payment_type"]
        order_payment.amount=form["activate_order_payment_form"].cleaned_data["amount"]
        order_payment.save()
        subscription_detail_id = (Billing.objects.get(id=billing_id.id)).subscriptiondetail
        subscription_detail = SubscriptionDetail.objects.get(pk=subscription_detail_id.id)
        subscription_detail.current_plan=form["activate_subscription_form"].cleaned_data["subscriptionplan"].id
        subscription_detail.choosen_plan=form["activate_subscription_form"].cleaned_data["subscriptionplan"].id
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
        context["subscriptionplan"] = dumps(
            list(SubscriptionPlan.objects.values("id", "price"))
        )
        return context


@method_decorator([allowed_users(["ADMIN", "SUPERVISOR"])], name="dispatch")
class ActivateSubscriptionGagal(SuccessMessageMixin, BaseBreadcrumbMixin, UpdateView):
    model = Subscription
    success_message = _("Subscription successfully activated!")
    fields = ["expires"]
    crumbs = [
        ("Subscription", reverse_lazy("subscriptions:list_subscription")),
        ("Activate Subscription", reverse_lazy("subscriptions:activate_subscription")),
    ]
    template_name = "subscriptions/form_subscription.html"
    success_url = reverse_lazy("subscriptions:list_subscription")

    def form_valid(self, form):
        subscription = form.save()
        name_type = dict(
            {"name": self.request.user.name, "type": self.request.user.type}
        )
        subscription.active = True
        subscription.modified_by = name_type
        subscription.is_approved = True
        subscription.save()

        return super().form_valid(form)


@allowed_users(allowed_roles=["ADMIN", "SUPERVISOR"])
def deactivate_subscription(request, id):
    subscription = Subscription.objects.get(pk=id)
    name_type = dict({"name": request.user.name, "type": request.user.type})
    subscription.active = False
    subscription.modified_by = name_type
    subscription.is_approved = False
    subscription.save()
    messages.success(request, "Subscriptions successfully deactivated!")
    return redirect("subscriptions:list_subscription")


@method_decorator([sales_only], name="dispatch")
class SalesActivateSubscription(SuccessMessageMixin, BaseBreadcrumbMixin, UpdateView):
    model = Subscription
    success_message = _(
        mark_safe(
            "Subscription activation request has been successful! <br/>Please wait for the activation process."
        )
    )
    # fields = ["expires"]
    form_class = ActivateSubscriptionForm
    crumbs = [
        ("Subscription", reverse_lazy("subscriptions:list_subscription")),
        (
            "Activate Subscription",
            reverse_lazy("subscriptions:sales_activate_subscription"),
        ),
    ]
    template_name = "subscriptions/form_subscription.html"
    success_url = reverse_lazy("subscriptions:list_subscription")

    # def get_form_kwargs(self):
    #     kwargs = super(SalesActivateSubscription, self).get_form_kwargs()
    #     kwargs["request"] = self.request

    #     return kwargs

    def form_valid(self, form):
        name_type = dict(
            {"name": self.request.user.name, "type": self.request.user.type}
        )
        subscription = form.save()
        subscription.active = False
        subscription.modified_by = name_type
        subscription.is_approved = ""
        subscription.save()

        return super().form_valid(form)


@allowed_users(allowed_roles=["SALES"])
def sales_deactivate_subscription(request, id):
    subscription = Subscription.objects.get(pk=id)
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
class DetailBilling(ListView):
    model = Billing
    queryset = Billing.objects.all()
    template_name = "subscriptions/detail_billing.html"

    # def get_queryset(self):
    #     billing_id = self.request.billing.id
    #     subscription = Subscription.objects.filter(billing_id=billing_id).values_list("id")
    #     billing = Billing.objects.filter(id__in=subscription)

    #     return Subscription.objects.filter(billing_id__in=billing).order_by("-id")


@method_decorator([allowed_users(["ADMIN", "SUPERVISOR"])], name="dispatch")
class DetailApprovalRequest(DetailView):
    model = Subscription
    template_name = "subscriptions/detail_approval.html"


@allowed_users(allowed_roles=["ADMIN", "SUPERVISOR"])
def accept_subscription(request, id):
    subscription = Subscription.objects.get(pk=id)
    name_type = dict({"name": request.user.name, "type": request.user.type})
    # subscription.active = False
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
def decline_subscription(request, id):
    subscription = Subscription.objects.get(pk=id)
    name_type = dict({"name": request.user.name, "type": request.user.type})
    # subscription.active = True
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
