from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db import connection
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView, CreateView, ListView


from .models import Subscription, SubscriptionPlan
from .forms import SubscriptionPlanAddForm, SubscriptionAddForm, SubscriptionPlanEditForm
from kawn_subscriptions_manager.decorators import supervisor_only, sales_only


# Create your views here.
@method_decorator([login_required, supervisor_only], name='dispatch')
class ListSubscriptionPlan(LoginRequiredMixin, ListView):
    model = SubscriptionPlan
    template_name = 'subscriptions/list_subscription_plan.html'
    queryset = SubscriptionPlan.objects.all()

list_subscription_plan= ListSubscriptionPlan.as_view()


@method_decorator([login_required, supervisor_only], name='dispatch')
class AddSubscriptionPlan(LoginRequiredMixin, CreateView):
    model = SubscriptionPlan
    form_class = SubscriptionPlanAddForm
    # fields = ['name','duration', 'price']
    success_message = _("Subscription plan successfully added")
    template_name = 'subscriptions/add_subscription_plan.html'

    def form_valid(self, form):
        subscriptionplan = form.save()
        return redirect('subscriptions:listSubscriptionPlan')

add_subscription_plan= AddSubscriptionPlan.as_view()


@method_decorator([login_required, supervisor_only], name='dispatch')
class ListUserSubscription(LoginRequiredMixin, ListView):
    model = Subscription
    template_name = 'subscriptions/list_user_subscriptions.html'
    # queryset = Subscription.objects.all().
    context_object_name = 'results'

    def get_context_data(self, **kwargs):
        cursor = connection.cursor()
        cursor.execute("SELECT u.name as user_name, usp.name as usp_name, us.start_date, us.end_date, DATE_PART('day', us.end_date - now()) as remaining_duration FROM subscriptions_subscription us INNER JOIN subscriptions_subscriptionplan usp ON usp.id = us.subscriptionplan_id INNER JOIN users_user u ON u.id = us.user_id")
        results = cursor.fetchall()
        context = super().get_context_data(**kwargs)
        context["results"] = results
        # var_dump(results)

        return context 

list_user_subscription= ListUserSubscription.as_view()


@method_decorator([login_required, sales_only], name='dispatch')
class SubscribeDetail(LoginRequiredMixin, CreateView):
    model = Subscription
    form_class = SubscriptionAddForm
    template_name = 'subscriptions/subscriptions.html'
    success_url = reverse_lazy('users:home')

subscribe_detail = SubscribeDetail.as_view()


@method_decorator([login_required, supervisor_only], name='dispatch')
class EditSubscriptionPlan(LoginRequiredMixin, UpdateView):
    model = SubscriptionPlan
    form_class = SubscriptionPlanEditForm
    template_name = 'subscriptions/edit_subscription_plan.html'
    context_object_name = 'results'

edit_subscription_plan = EditSubscriptionPlan.as_view()
