from django.contrib.auth import get_user_model
from kawn_subscriptions_manager.users.models import SubscriptionPlan, Subscription
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView, CreateView, ListView
from django.contrib.auth.views import LoginView 
from django.shortcuts import redirect, render
from django.core.exceptions import PermissionDenied
from .models import User, Subscription, SubscriptionPlan
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from kawn_subscriptions_manager.users.forms import SupervisorAddForm, SubscriptionPlanAddForm, SubscriptionAddForm, SubscriptionPlanEditForm
from .decorators import unauthenticated_user, allowed_users, admin_only, supervisor_only, sales_only
from django.db import connection
from var_dump import var_dump

User = get_user_model()

class UserDetailView(LoginRequiredMixin, DetailView, PermissionDenied):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"

user_detail_view = UserDetailView.as_view()

@login_required
def profile(request):
    return render(request, 'users/profile.html')


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

    model = User
    fields = ["username", "email", "name", "first_name", "last_name"]
    success_message = _("Information successfully updated")

    def get_success_url(self):
        assert (
            self.request.user.is_authenticated
        )  # for mypy to know that the user is authenticated
        return self.request.user.get_absolute_url()

    def get_object(self):
        return self.request.user

user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        # return reverse("users:detail", kwargs={"username": self.request.user.username})
        return redirect("users:update")

user_redirect_view = UserRedirectView.as_view()


def home(request):

    model = SubscriptionPlan
    sp = model.objects.all()

    if request.user.is_authenticated:
        if request.user.type == "SALES":
            # return render(request, 'users/sales/home_sales.html')
            return render(request, 'users/sales/home_sales.html', {'SubscriptionPlans' : sp})
        elif request.user.type == "SUPERVISOR":
            return render(request, 'users/supervisor/home_supervisor.html')
        else:
            return render(request, 'users/admin/home_admin.html')
    return redirect('account_login')


@method_decorator([login_required, admin_only], name='dispatch')
class AddSupervisor(LoginRequiredMixin, CreateView):
    model = User
    form_class = SupervisorAddForm
    # fields = ['username','email', 'password']
    success_message = _("Supervisor successfully added")
    template_name = 'users/admin/add_supervisor.html'

    def form_valid(self, form):
        user = form.save()
        # login(self.request, user)
        return redirect('users:home')

add_supervisor = AddSupervisor.as_view()


@method_decorator([login_required, supervisor_only], name='dispatch')
class ListSubscriptionPlan(LoginRequiredMixin, ListView):
    model = SubscriptionPlan
    template_name = 'users/supervisor/list_subscription_plan.html'
    context_object_name = 'results'

    def get_context_data(self, **kwargs):
        cursor = connection.cursor()
        cursor.execute("SELECT name, duration, price FROM users_subscriptionplan")
        results = cursor.fetchall()
        context = super().get_context_data(**kwargs)
        context["results"] = results
        # var_dump(results)

        return context 

list_subscription_plan= ListSubscriptionPlan.as_view()


@method_decorator([login_required, supervisor_only], name='dispatch')
class AddSubscriptionPlan(LoginRequiredMixin, CreateView):
    model = SubscriptionPlan
    form_class = SubscriptionPlanAddForm
    # fields = ['name','duration', 'price']
    success_message = _("Subscription plan successfully added")
    template_name = 'users/supervisor/add_subscription_plan.html'

    def form_valid(self, form):
        subscriptionplan = form.save()
        return redirect('users:home')

add_subscription_plan= AddSubscriptionPlan.as_view()


@method_decorator([login_required, supervisor_only], name='dispatch')
class ListUserSubscription(LoginRequiredMixin, ListView):
    model = Subscription
    template_name = 'users/supervisor/list_user_subscriptions.html'
    context_object_name = 'results'

    def get_context_data(self, **kwargs):
        cursor = connection.cursor()
        cursor.execute("SELECT u.name as user_name, usp.name as usp_name, us.start_date, us.end_date, DATE_PART('day', us.end_date - now()) as remaining_duration FROM users_subscription us INNER JOIN users_subscriptionplan usp ON usp.id = us.subscriptionplan_id INNER JOIN users_user u ON u.id = us.user_id")
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
    template_name = 'users/sales/subscriptions.html'
    success_url = reverse_lazy('users:home')

subscribe_detail = SubscribeDetail.as_view()

@method_decorator([login_required, supervisor_only], name='dispatch')
class EditSubscriptionPlan(LoginRequiredMixin, UpdateView):
    model = SubscriptionPlan
    form_class = SubscriptionPlanEditForm
    template_name = 'users/supervisor/edit_subscription_plan.html'
    context_object_name = 'results'

edit_subscription_plan = EditSubscriptionPlan.as_view()