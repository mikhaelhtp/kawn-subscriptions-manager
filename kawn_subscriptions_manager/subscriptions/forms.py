from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django import forms
from django.forms import ModelForm

from kawn_subscriptions_manager.clients.models import Client
from .models import SubscriptionPlan, Subscription

# class SubscriptionPlanAddForm(ModelForm):

#     class Meta:
#         model = SubscriptionPlan
#         fields = ['name','duration', 'price']

#     def save(self, commit=True):
#         subscriptionplan = super().save(commit=False)
#         if commit:
#             subscriptionplan.save()
#         return subscriptionplan


# class SubscriptionAddForm(ModelForm):

#     class Meta:
#         model = Subscription
#         fields = ['user','subscriptionplan', 'start_date', 'end_date']
#         widgets = {
#             'start_date': forms.DateInput({'type':'date'}),
#             'end_date': forms.DateInput({'type':'date'}),
#         }


# class SubscriptionPlanUpdateForm(ModelForm):

#     class Meta:
#         model = SubscriptionPlan
#         fields = ['name', 'duration', 'price']


class AddClientSubscriptionForm(ModelForm):

    class Meta:
        model = Subscription
        # start_date = forms.DateTimeInput(input_formats=['%m/%d/%Y %H:%M'])
        # end_date = forms.DateTimeInput(input_formats=['%m/%d/%Y %H:%M'])
        fields = ["subscriptionplan", "client", "start_date", "end_date"]
        widgets = {
            'start_date': forms.DateTimeInput({'type':'date'}),
            'end_date': forms.DateTimeInput({'type':'date'}),
        }

    def __init__(self, user, *args, **kwargs):
        super(AddClientSubscriptionForm, self).__init__(*args, **kwargs)
        client = Client.objects.filter(user_id=user.id, is_active=True)
        clients = [(i.id, i.name) for i in client]

        subscriptionplan = SubscriptionPlan.objects.filter(is_active=True)
        subscriptionplans = [(i.id, i.name) for i in subscriptionplan]

        self.fields['client'].choices = clients
        self.fields['subscriptionplan'].choices = subscriptionplans
        self.fields['subscriptionplan'].label = "Subscription Plan"

    # def check_status(self):
    #     now = timezone.now()
    #     if now > self.end_date and self.is_active:
    #         self.is_active = False
    #         self.save()
    #         return False
    #     return self.is_active

    # def save(self, commit=True):
    #     subscription = super().save(commit=False)
    #     if commit:
    #         subscription.save()
    #     return subscription