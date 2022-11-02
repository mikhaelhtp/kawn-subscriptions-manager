import datetime
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django import forms
from django.forms import ModelForm

from kawn_subscriptions_manager.clients.models import Client, Outlet
from .models import SubscriptionPlan, Subscription

today = datetime.date.today() + datetime.timedelta(days=1)


class AddSubscriptionForm(ModelForm):
    billing_date = forms.DateField(
        widget=forms.DateTimeInput(attrs={"type": "date", "value": today}),
        required=True,
    )
    expires = forms.DateField(
        widget=forms.DateTimeInput(
            attrs={"min": today, "value": today, "type": "date"}
        ),
        required=True,
    )

    class Meta:
        model = Subscription
        input_type = "date"
        fields = ["subscriptionplan", "outlet", "billing_date", "expires"]

    def __init__(self, user, *args, **kwargs):
        super(AddSubscriptionForm, self).__init__(*args, **kwargs)
        client = Client.objects.values_list("id").filter(user_id=user.id)
        subscription = Subscription.objects.values_list("outlet_id")
        outlet = Outlet.objects.exclude(id__in=subscription).filter(
            client_id__in=client
        )
        outlets = [(i.id, i.name) for i in outlet]

        subscriptionplan = SubscriptionPlan.objects.filter(is_active=True)
        subscriptionplans = [(i.id, i.name) for i in subscriptionplan]

        self.fields["outlet"].choices = outlets
        self.fields["subscriptionplan"].choices = subscriptionplans
        self.fields["subscriptionplan"].label = "Subscription Plan"
