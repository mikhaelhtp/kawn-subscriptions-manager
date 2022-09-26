from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db import connection
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.generic import UpdateView, CreateView, ListView, DeleteView

from .models import Subscription, SubscriptionPlan
from .forms import SubscriptionPlanUpdateForm, AddClientSubscriptionForm
from kawn_subscriptions_manager.decorators import supervisor_only, sales_only

# Create your views here.
@method_decorator([login_required, supervisor_only], name='dispatch')
class ListSubscriptionPlan(LoginRequiredMixin, ListView):

    model = SubscriptionPlan
    template_name = 'subscriptions/subscription_plans/list_subscription_plan.html'
    queryset = SubscriptionPlan.objects.all()

list_subscription_plan= ListSubscriptionPlan.as_view()


@method_decorator([login_required, supervisor_only], name='dispatch')
class AddSubscriptionPlan(LoginRequiredMixin, SuccessMessageMixin, CreateView):

    model = SubscriptionPlan
    fields = ['name','duration', 'price']
    template_name = 'subscriptions/subscription_plans/add_subscription_plan.html'
    success_url = reverse_lazy('subscriptions:listSubscriptionPlan')
    success_message = ("Subscription plan successfully added!")

add_subscription_plan= AddSubscriptionPlan.as_view()


@method_decorator([login_required, supervisor_only], name='dispatch')
class UpdateSubscriptionPlan(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

    model = SubscriptionPlan
    form_class = SubscriptionPlanUpdateForm
    template_name = 'subscriptions/subscription_plans/update_subscription_plan.html'
    success_url = reverse_lazy('subscriptions:listSubscriptionPlan')
    success_message = ("Subscription plan successfully updated!")

update_subscription_plan = UpdateSubscriptionPlan.as_view()


@method_decorator([login_required, supervisor_only], name='dispatch')
class delateSubscriptionPlan(LoginRequiredMixin, SuccessMessageMixin, DeleteView):

    model = SubscriptionPlan
    success_url = reverse_lazy('subscriptions:listSubscriptionPlan')
    success_message = ("Subscription plan successfully delated!")

delate_subscription_plan = delateSubscriptionPlan.as_view()


@login_required()
def subscriptionplan_deactivate(request, id):
    subscriptionplan = SubscriptionPlan.objects.get(pk=id)
    subscriptionplan.is_active = False
    subscriptionplan.save()
    messages.success(request, "Subscription plan has been successfully deactivated!")
    return redirect('subscriptions:listSubscriptionPlan')


@login_required()
def subscriptionplan_activate(request, id):
    subscriptionplan = SubscriptionPlan.objects.get(pk=id)
    subscriptionplan.is_active = True
    subscriptionplan.save()
    messages.success(request, "Subscription plan has been successfully activated!")
    return redirect('subscriptions:listSubscriptionPlan')


# @method_decorator([login_required, supervisor_only], name='dispatch')
# class customerSubscription(LoginRequiredMixin, ListView):

#     model = Subscription
#     template_name = 'subscriptions/client_subscriptions/customer_subscriptions.html'
#     context_object_name = 'results'

#     def get_context_data(self, **kwargs):
#         cursor = connection.cursor()
#         cursor.execute("SELECT u.name as user_name, usp.name as usp_name, us.start_date, us.end_date, DATE_PART('day', us.end_date - now()) as remaining_duration FROM subscriptions_subscription us INNER JOIN subscriptions_subscriptionplan usp ON usp.id = us.subscriptionplan_id INNER JOIN users_user u ON u.id = us.user_id")
#         results = cursor.fetchall()
#         context = super().get_context_data(**kwargs)
#         context["results"] = results

#         return context 

# customer_subscription= customerSubscription.as_view()


@method_decorator([login_required], name='dispatch')
class ListClientSubscription(LoginRequiredMixin, ListView):
    model = Subscription
    template_name = 'subscriptions/client_subscriptions/list_client_subscription.html'
    # queryset = Subscription.objects.all().
    context_object_name = 'results'

    def get_context_data(self, **kwargs):
        userid = self.request.user.id
        user_role = self.request.user.type
        cursor = connection.cursor()
        if user_role == "SALES":
            cursor.execute("SELECT cc.name as client_name, uu.name as sales_name, ssp.name as subscription_plan_name, ss.start_date, ss.end_date, DATE_PART('day', ss.end_date - now()) as remaining_duration, ss.is_active, ss.id FROM subscriptions_subscription ss INNER JOIN subscriptions_subscriptionplan ssp ON ss.subscriptionplan_id = ssp.id INNER JOIN clients_client cc ON cc.id = ss.client_id INNER JOIN users_user uu ON uu.id = cc.user_id WHERE cc.user_id="+str(userid))
        else:
            cursor.execute("SELECT cc.name as client_name, uu.name as sales_name, ssp.name as subscription_plan_name, ss.start_date, ss.end_date, DATE_PART('day', ss.end_date - now()) as remaining_duration, ss.is_active, ss.id FROM subscriptions_subscription ss INNER JOIN subscriptions_subscriptionplan ssp ON ss.subscriptionplan_id = ssp.id INNER JOIN clients_client cc ON cc.id = ss.client_id INNER JOIN users_user uu ON uu.id = cc.user_id")
        results = cursor.fetchall()
        context = super().get_context_data(**kwargs)
        context["results"] = results
        # var_dump(results)

        return context

list_client_subscription = ListClientSubscription.as_view()


@method_decorator([login_required, sales_only], name='dispatch')
class AddClientSubscription(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Subscription
    template_name = 'subscriptions/client_subscriptions/add_client_subscription.html'
    success_url = reverse_lazy('subscriptions:listClientSubscription')
    success_message = _("Subscription successfully added")
    # form_class = AddClientSubscriptionForm
    # form_class.fields['price'].initial = SubscriptionPlan.objects.filter(price=request.price)

    def get_form(self):
        if self.request.method == 'POST':
            return AddClientSubscriptionForm(data=self.request.POST, user=self.request.user)
        else:
            return AddClientSubscriptionForm(user=self.request.user)

add_client_subscription = AddClientSubscription.as_view()


@login_required()
def deactivate_client_subscription(request, id):
    subscription = Subscription.objects.get(pk=id)
    subscription.is_active = False
    subscription.save()
    messages.success(request, "Client subscription has been successfully deactivated!")
    return redirect('subscriptions:listClientSubscription')


@login_required()
def activate_client_subscription(request, id):
    subscription = Subscription.objects.get(pk=id)
    subscription.is_active = True
    subscription.save()
    messages.success(request, "Client subscription has been successfully activated!")
    return redirect('subscriptions:listClientSubscription')