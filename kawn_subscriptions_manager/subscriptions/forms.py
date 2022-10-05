from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django import forms
from django.forms import ModelForm

from kawn_subscriptions_manager.clients.models import Client, Outlet
from .models import SubscriptionPlan, Subscription


class AddSubscriptionForm(ModelForm):
    class Meta:
        model = Subscription
        fields = ["subscriptionplan", "outlet", "start_date", "end_date"]
        widgets = {
            "start_date": forms.DateTimeInput({"type": "date"}),
            "end_date": forms.DateTimeInput({"type": "date"}),
        }

    def __init__(self, user, *args, **kwargs):
        super(AddSubscriptionForm, self).__init__(*args, **kwargs)
        client = Client.objects.values_list('id').filter(user_id=user.id)
        outlet = Outlet.objects.filter(client_id__in=client)
        outlets = [(i.id, i.name) for i in outlet]

        subscriptionplan = SubscriptionPlan.objects.filter(is_active=True)
        subscriptionplans = [(i.id, i.name) for i in subscriptionplan]

        self.fields["outlet"].choices = outlets
        self.fields["subscriptionplan"].choices = subscriptionplans
        self.fields["subscriptionplan"].label = "Subscription Plan"
