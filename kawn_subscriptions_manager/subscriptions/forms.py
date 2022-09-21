from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django import forms
from django.forms import ModelForm

from .models import SubscriptionPlan, Subscription

class SubscriptionPlanAddForm(ModelForm):

    class Meta:
        model = SubscriptionPlan
        fields = ['name','duration', 'price']

    def save(self, commit=True):
        subscriptionplan = super().save(commit=False)
        if commit:
            subscriptionplan.save()
        return subscriptionplan


class SubscriptionAddForm(ModelForm):

    class Meta:
        model = Subscription
        fields = ['user','subscriptionplan', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput({'type':'date'}),
            'end_date': forms.DateInput({'type':'date'}),
        }

    def save(self, commit=True):
        subscription = super().save(commit=False)
        if commit:
            subscription.save()
        return subscription


class SubscriptionPlanUpdateForm(ModelForm):

    class Meta:
        model = SubscriptionPlan
        fields = ['name', 'duration', 'price']