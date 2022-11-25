from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator
from django.utils.safestring import mark_safe
from django.shortcuts import redirect, render
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin
from django_tables2.export.views import ExportMixin
from view_breadcrumbs import ListBreadcrumbMixin, BaseBreadcrumbMixin
from django_filters.views import FilterView
from django.views.generic import (
    DetailView,
    RedirectView,
    UpdateView,
    CreateView,
    ListView,
    DeleteView,
)

from .tables import UserTable
from .filters import UserFilter
from .models import User
from .forms import UsersEditForm
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
        assert self.request.user.is_authenticated
        return self.request.user.get_absolute_url()

    def get_object(self):
        return self.request.user


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        # return reverse("users:detail", kwargs={"username": self.request.user.username})
        return redirect("users:update")


@method_decorator([admin_only], name="dispatch")
class ListUsers(
    SuccessMessageMixin, ListBreadcrumbMixin,ListView, ExportMixin, SingleTableMixin, FilterView
):
    model = User
    filterset_class = UserFilter
    table_class = UserTable
    context_object_name = "results"
    template_name = "users/user_list.html"
    export_formats = ("csv", "tsv", "xlsx", "json")
    exclude_columns = (
        "id",
        "password",
        "first_name",
        "last_name",
        "last_login",
        "date_joined",
        "is_superuser",
        "is_staff",
        "is_active",
        "is_active",
    )

    def get_queryset(self):
        return User.objects.raw(
            """SELECT b.id, b.username, b.email, b.name, b.is_active, b.type, am.verified 
                                FROM account_emailaddress AS am 
                                INNER JOIN users_user AS b ON am.user_id = b.id
                                ORDER BY b.type"""
        )
        
    def get_table_kwargs(self):
        return {"template_name": "users/user_list.html"}


@method_decorator([admin_only], name="dispatch")
class AddUsers(SuccessMessageMixin, BaseBreadcrumbMixin, CreateView):
    model = User
    fields = ["username", "name", "email", "type"]
    template_name = "users/admin/add_users.html"
    crumbs = [
        ("Users", reverse_lazy("users:user_list")),
        ("Add User", reverse_lazy("users:add_users")),
    ]
    success_message = _(
        "Account has been created successfully! <br/>Account details have been sent to the respective email."
    )
    success_url = reverse_lazy("users:user_list")

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, mark_safe(self.success_message))

        html = render_to_string(
            "account/email_account_creation.html",
            {
                "email": form.cleaned_data["email"],
                "access": form.cleaned_data["type"],
                "domain": self.request.scheme+"://"+self.request.META['HTTP_HOST']
            },
        )

        send_mail(
            "[Kawn Subscriptions Manager] Account Creation",
            "[Kawn Subscriptions Manager] Account Creation",
            self.request.user.email,
            [form.cleaned_data["email"]],
            html_message=html,
            fail_silently=False,
        )
        return redirect("users:user_list")


@method_decorator([admin_only], name="dispatch")
class EditUsers(SuccessMessageMixin, BaseBreadcrumbMixin, UpdateView):
    model = User
    form_class = UsersEditForm
    template_name = "users/admin/edit_users.html"
    crumbs = [
        ("Users", reverse_lazy("users:user_list")),
        ("Edit User", reverse_lazy("users:edit_users")),
    ]
    success_message = _("User successfully updated")
    success_url = reverse_lazy("users:user_list")


@method_decorator([admin_only], name="dispatch")
class DeleteUsers(SuccessMessageMixin, DeleteView):
    model = User
    success_url = reverse_lazy("users:user_list")
    success_message = _("User successfully deleted")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(DeleteUsers, self).delete(request, *args, **kwargs)


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
