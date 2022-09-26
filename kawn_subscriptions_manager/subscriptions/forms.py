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


class SubscriptionPlanUpdateForm(ModelForm):

    class Meta:
        model = SubscriptionPlan
        fields = ['name', 'duration', 'price']


class AddClientSubscriptionForm(ModelForm):

    class Meta:
        model = Subscription
        fields = ["subscriptionplan", "client", "start_date", "end_date"]
        widgets = {
            'start_date': forms.DateTimeInput({'type':'date'}),
            'end_date': forms.DateTimeInput({'type':'date'}),
        }

    def __init__(self, user, *args, **kwargs):
        super(AddClientSubscriptionForm, self).__init__(*args, **kwargs)
        # this is pseudo code but you should get all variants
        # then get the product related to each variant
        client = Client.objects.filter(user_id=user.id)
        clients = [(i.id, i.name) for i in client]

        subscriptionplan = SubscriptionPlan.objects.all()
        subscriptionplans = [(i.id, i.name) for i in subscriptionplan]

        self.fields['client'].choices = clients
        self.fields['subscriptionplan'].choices = subscriptionplans
        self.fields['subscriptionplan'].label = "Subscription Plan"

    def save(self, commit=True):
        subscription = super().save(commit=False)
        if commit:
            subscription.save()
        return subscription