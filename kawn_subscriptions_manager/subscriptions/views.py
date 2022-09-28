from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db import connection
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.generic import UpdateView, CreateView, ListView, DeleteView

from .models import Subscription, SubscriptionPlan
from .forms import AddClientSubscriptionForm
from kawn_subscriptions_manager.decorators import allowed_users, sales_only


@method_decorator([login_required], name="dispatch")
class ListSubscriptionPlan(LoginRequiredMixin, ListView):
    model = SubscriptionPlan
    template_name = "subscriptions/subscription_plans/list_subscription_plan.html"
    queryset = SubscriptionPlan.objects.all()


@method_decorator(
    [login_required, allowed_users(["ADMIN", "SUPERVISOR"])], name="dispatch"
)
class AddSubscriptionPlan(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = SubscriptionPlan
    fields = ["name", "duration", "price"]
    template_name = "subscriptions/subscription_plans/form_subscription_plan.html"
    success_url = reverse_lazy("subscriptions:list_subscription_plan")
    success_message = "Subscription plans successfully added!"


@method_decorator(
    [login_required, allowed_users(["ADMIN", "SUPERVISOR"])], name="dispatch"
)
class UpdateSubscriptionPlan(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = SubscriptionPlan
    fields = ["name", "duration", "price"]
    template_name = "subscriptions/subscription_plans/form_subscription_plan.html"
    success_url = reverse_lazy("subscriptions:list_subscription_plan")
    success_message = "Subscription plans successfully updated!"


@method_decorator(
    [login_required, allowed_users(["ADMIN", "SUPERVISOR"])], name="dispatch"
)
class DeleteSubscriptionPlan(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = SubscriptionPlan
    success_url = reverse_lazy("subscriptions:list_subscription_plan")
    success_message = "Subscription plans successfully delated!"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(DeleteSubscriptionPlan, self).delete(request, *args, **kwargs)


@login_required()
@allowed_users(allowed_roles=["ADMIN", "SUPERVISOR"])
def deactivate_subscription_plan(request, id):
    subscriptionplan = SubscriptionPlan.objects.get(pk=id)
    subscriptionplan.is_active = False
    subscriptionplan.save()
    messages.success(request, "Subscription plans has been successfully deactivated!")
    return redirect("subscriptions:list_subscription_plan")


@login_required()
@allowed_users(allowed_roles=["ADMIN", "SUPERVISOR"])
# @supervisor_only
def activate_subscription_plan(request, id):
    subscriptionplan = SubscriptionPlan.objects.get(pk=id)
    subscriptionplan.is_active = True
    subscriptionplan.save()
    messages.success(request, "Subscription plans has been successfully activated!")
    return redirect("subscriptions:list_subscription_plan")


@method_decorator([login_required], name="dispatch")
class ListClientSubscription(LoginRequiredMixin, ListView):
    model = Subscription
    template_name = "subscriptions/client_subscriptions/list_client_subscription.html"
    context_object_name = "results"
    queryset = Subscription.objects.all()

    def get_context_data(self, **kwargs):
        userid = self.request.user.id
        user_role = self.request.user.type
        cursor = connection.cursor()
        if user_role == "SALES":
            cursor.execute(
                "SELECT cc.business_name as outlet_name, uu.name as sales_name, ssp.name as subscription_plan_name, ss.start_date, ss.end_date, DATE_PART('day', ss.end_date - now()) as remaining_duration, ss.is_active, ss.id FROM subscriptions_subscription ss INNER JOIN subscriptions_subscriptionplan ssp ON ss.subscriptionplan_id = ssp.id INNER JOIN clients_client cc ON cc.id = ss.client_id INNER JOIN users_user uu ON uu.id = cc.user_id WHERE cc.user_id="
                + str(userid)
                + "ORDER BY ss.id"
            )
        else:
            cursor.execute(
                "SELECT cc.business_name as outlet_name, uu.name as sales_name, ssp.name as subscription_plan_name, ss.start_date, ss.end_date, DATE_PART('day', ss.end_date - now()) as remaining_duration, ss.is_active, ss.id FROM subscriptions_subscription ss INNER JOIN subscriptions_subscriptionplan ssp ON ss.subscriptionplan_id = ssp.id INNER JOIN clients_client cc ON cc.id = ss.client_id INNER JOIN users_user uu ON uu.id = cc.user_id ORDER BY ss.id"
            )
        results = cursor.fetchall()
        context = super().get_context_data(**kwargs)
        context["results"] = results

        now = timezone.now()
        Subscription.objects.filter(end_date__lte=now).update(is_active=False)
        # var_dump(results)

        return context


@method_decorator([login_required, sales_only], name="dispatch")
class AddClientSubscription(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Subscription
    template_name = "subscriptions/client_subscriptions/form_client_subscription.html"
    success_url = reverse_lazy("subscriptions:list_client_subscription")
    success_message = _("Subscriptions successfully added")

    def get_form(self):
        if self.request.method == "POST":
            return AddClientSubscriptionForm(
                data=self.request.POST, user=self.request.user
            )
        else:
            return AddClientSubscriptionForm(user=self.request.user)


@method_decorator([login_required, sales_only], name="dispatch")
class UpdateClientSubscription(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Subscription
    success_message = _("Subscription successfully updated")
    fields = ["start_date", "end_date"]
    template_name = "subscriptions/client_subscriptions/form_client_subscription.html"
    success_url = reverse_lazy("subscriptions:list_client_subscription")

    def form_valid(self, form):
        subscription = form.save()
        now = timezone.now()
        if form.cleaned_data["end_date"] > now:
            subscription.is_active = True
            subscription.save()
        else:
            subscription.is_active = False
            subscription.save()
        return super().form_valid(form)


@login_required()
@allowed_users(allowed_roles=["ADMIN", "SALES"])
def deactivate_client_subscription(request, id):
    subscription = Subscription.objects.get(pk=id)
    subscription.is_active = False
    subscription.save()
    messages.success(request, "Client subscriptions has been deactivated successfully!")
    return redirect("subscriptions:list_client_subscription")
