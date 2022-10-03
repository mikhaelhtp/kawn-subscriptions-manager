from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.utils.decorators import method_decorator
from django.utils.safestring import mark_safe
from django.shortcuts import redirect, render
from django.core.mail import send_mail
from django.core.exceptions import PermissionDenied
from django.template.loader import render_to_string
from django.views.generic import (
    DetailView,
    RedirectView,
    UpdateView,
    CreateView,
    ListView,
    DeleteView,
)

from .models import User
from .forms import UsersAddForm, UsersEditForm
from kawn_subscriptions_manager.decorators import (
    admin_only,
)

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView, PermissionDenied):
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


@login_required
def profile(request):
    return render(request, "users/profile.html")


def forgotpassword(request):
    return render(request, "users/password_reset.html")


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


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        # return reverse("users:detail", kwargs={"username": self.request.user.username})
        return redirect("users:update")


@method_decorator([login_required, admin_only], name="dispatch")
class AddUsers(SuccessMessageMixin, CreateView):
    model = User
    form_class = UsersAddForm
    template_name = "users/admin/add_users.html"
    success_message = _(
        "Account has been created successfully! <br/>Account details have been sent to the respective email."
    )
    success_url = reverse_lazy("users:add_user")

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, mark_safe(self.success_message))

        html = render_to_string(
            "account/email_account_creation.html",
            {
                "email": form.cleaned_data["email"],
                "username": form.cleaned_data["username"],
                "password": form.cleaned_data["password1"],
                "access": form.cleaned_data["type"],
            },
        )

        send_mail(
            "[Kawn Subscriptions Manager] Account Creation",
            "This is the message",
            self.request.user.email,
            [form.cleaned_data["email"]],
            html_message=html,
            fail_silently=False,
        )
        return redirect("users:add_users")


@method_decorator([login_required, admin_only], name="dispatch")
class EditUsers(SuccessMessageMixin, UpdateView):
    model = User
    form_class = UsersEditForm
    template_name = "users/admin/edit_users.html"
    success_message = _("User successfully updated")
    success_url = reverse_lazy("users:list_users")


@method_decorator([login_required, admin_only], name="dispatch")
class DeleteUsers(SuccessMessageMixin, DeleteView):
    model = User
    success_url = reverse_lazy("users:list_users")
    success_message = _("User successfully deleted")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(DeleteUsers, self).delete(request, *args, **kwargs)


@method_decorator([login_required, admin_only], name="dispatch")
class ListUsers(SuccessMessageMixin, ListView):
    model = User
    template_name = "users/user_list.html"
    # queryset = User.objects.all().order_by('type')

    def get_queryset(self):
        return User.objects.raw(
            """SELECT b.id, b.username, b.email, b.name, b.is_staff, b.is_active, b.type, am.verified 
                                FROM account_emailaddress AS am 
                                INNER JOIN users_user AS b ON am.user_id = b.id
                                ORDER BY b.type"""
        )


# @login_required
# @admin_only
# def invite(request):

#     if request.method == 'GET':
#         form = UserInviteForm()
#     else:
#         form = UserInviteForm(request.POST)
#         if form.is_valid():
#             from_email = request.user.email
#             to = form.cleaned_data['to']
#             subject = form.cleaned_data['subject']
#             message = form.cleaned_data['message']
#             try:
#                 send_mail(from_email, subject, message, [to], fail_silently=False)
#             except BadHeaderError:
#                 return HttpResponse('Invalid header found.')
#             return redirect('users:inviteUsers')
#     return render(request, "users/admin/invite_users.html", {'form': form})
