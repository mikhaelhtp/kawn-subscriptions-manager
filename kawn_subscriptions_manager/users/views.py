from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView, CreateView
from django.contrib.auth.views import LoginView 
from django.shortcuts import redirect, render
from django.core.exceptions import PermissionDenied

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from kawn_subscriptions_manager.users.forms import SupervisorAddForm
from .decorators import unauthenticated_user, allowed_users, admin_only

User = get_user_model()

class UserDetailView(LoginRequiredMixin, DetailView, PermissionDenied):

    model = User
    slug_field = "id"
    slug_url_kwarg = "id"

user_detail_view = UserDetailView.as_view()

@login_required
def profile(request):
    return render(request, 'users/profile.html')


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

    model = User
    fields = ["name"]
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
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()

def home(request):
    if request.user.is_authenticated:
        if request.user.type == "SALES":
            return render(request, 'users/sales/home_sales.html')
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