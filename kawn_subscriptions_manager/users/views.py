from email import message
import email
from multiprocessing import context, get_context
from signal import Signals
from urllib import request
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView, CreateView, ListView, DeleteView
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView, CreateView
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string

from kawn_subscriptions_manager.subscriptions import forms
from .models import User
from .forms import UsersAddForm, UsersEditForm
from kawn_subscriptions_manager.decorators import admin_only
from django import forms

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView, PermissionDenied):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


@login_required
def profile(request):
    return render(request, 'users/profile.html')


def forgotpassword(request):
    return render(request, 'users/password_reset.html')


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
    form_class = UsersAddForm
    success_message = _("Users successfully added")
    template_name = 'users/admin/add_users.html'

    def form_valid(self, form):
        user = form.save()
        
        html = render_to_string('account/message.html', {
                'email': form.cleaned_data['email'],
                'username': form.cleaned_data['username'],
                'password': form.cleaned_data['password1'],
                'access': form.cleaned_data['type']
            })
        
        send_mail(
            'Account Created by Admin',
            'This is the message',
            self.request.user.email,
            [form.cleaned_data['email']],
            html_message=html,
            fail_silently=False
        )
        return redirect('users:listUsers')


add_users = AddUsers.as_view()


@method_decorator([login_required, admin_only], name='dispatch')
class EditUsers(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = UsersEditForm
    template_name = 'users/admin/edit_users.html'
    success_message = _("User successfully updated")
    success_url = reverse_lazy('users:listUsers')


edit_users = EditUsers.as_view()


@method_decorator([login_required, admin_only], name='dispatch')
class DeleteUsers(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = User
    success_url = reverse_lazy('users:listUsers')
    success_message = _("User successfully deleted")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(DeleteUsers, self).delete(request, *args, **kwargs)


delete_users = DeleteUsers.as_view()


@method_decorator([login_required, admin_only], name='dispatch')
class ListUsers(LoginRequiredMixin, SuccessMessageMixin, ListView):
    model = User
    template_name = 'users/user_list.html'
    queryset = User.objects.all().order_by('type')


list_users = ListUsers.as_view()


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