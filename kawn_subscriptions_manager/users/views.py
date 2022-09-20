from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView, CreateView, ListView
from django.contrib.auth.views import LoginView 
from django.shortcuts import redirect, render
from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .models import User
from .forms import SupervisorAddForm
from kawn_subscriptions_manager.decorators import admin_only

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


@method_decorator([login_required, admin_only], name='dispatch')
class AddUsers(LoginRequiredMixin, CreateView):
    model = User
    form_class = SupervisorAddForm
    # fields = ['username','email', 'password']
    success_message = _("Users successfully added")
    template_name = 'users/admin/add_users.html'

    def form_valid(self, form):
        user = form.save()
        # login(self.request, user)
        return redirect('users:home')

add_users = AddUsers.as_view()


