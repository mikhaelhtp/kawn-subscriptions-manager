import datetime
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django import forms
from django.forms import ModelForm
from betterforms.multiform import MultiModelForm

from kawn_subscriptions_manager.clients.models import Client, Outlet
from .models import SubscriptionPlan, Subscription, Billing, OrderPayment, SubscriptionDetail

today = datetime.date.today()
tomorow = datetime.date.today() + datetime.timedelta(days=1)


class OrderPaymentForm(ModelForm):
    class Meta:
        model = OrderPayment
        fields = ["payment_type", "amount"]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(OrderPaymentForm, self).__init__(*args, **kwargs)


class BillingForm(ModelForm):
    class Meta:
        model = Billing
        fields = ["price"]
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(BillingForm, self).__init__(*args, **kwargs)
        self.fields['price'].widget.attrs['readonly'] = True


class AddSubscriptionForm(ModelForm):
    billing_date = forms.DateField(
        widget=forms.DateTimeInput(attrs={"type": "date", "value": today}),
        required=True,
    )
    expires = forms.DateField(
        widget=forms.DateTimeInput(
            attrs={"min": tomorow, "value": tomorow, "type": "date"}
        ),
        required=True,
    )

    class Meta:
        model = Subscription
        input_type = "date"
        fields = ["subscriptionplan", "outlet", "billing_date", "expires"]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(AddSubscriptionForm, self).__init__(*args, **kwargs)
        user_id = self.request.user.id
        client = Client.objects.values_list("id").filter(user_id=user_id)
        subscription = Subscription.objects.values_list("outlet_id")
        outlet = Outlet.objects.exclude(id__in=subscription).filter(
            client_id__in=client
        )
        outlets = [(i.id, i.name) for i in outlet]

        subscriptionplan = SubscriptionPlan.objects.filter(is_active=True)
        subscriptionplans = [(i.id, i.name) for i in subscriptionplan]
        SUBPLAN = [("", "--------")] + subscriptionplans

        self.fields["outlet"].choices = outlets
        self.fields["subscriptionplan"].choices = SUBPLAN
        self.fields["subscriptionplan"].label = "Subscription Plan"


class SubscriptionMultiForm(MultiModelForm):
    form_classes = {
        "subscription_form": AddSubscriptionForm,
        "billing_form": BillingForm,
        "order_payment": OrderPaymentForm,
    }

    def get_form_args_kwargs(self, key, args, kwargs):
        fargs, fkwargs = super(SubscriptionMultiForm, self).get_form_args_kwargs(key, args, kwargs)
        fkwargs.update({
            'request': kwargs.get('request')
        })
        return fargs, fkwargs


class ActivateBillingForm(ModelForm):
    class Meta:
        model = Billing
        fields = ["price"]
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        outlet_id = kwargs.pop("outlet_id")
        super(ActivateBillingForm, self).__init__(*args, **kwargs)
        self.fields['price'].widget.attrs['readonly'] = True


class ActivateSubscriptionForm(ModelForm):
    
    outlet = forms.CharField(disabled=True, required=False)

    billing_date = forms.DateField(
        widget=forms.DateTimeInput(attrs={"type": "date", "value": today}),
        required=True,
    )

    expires = forms.DateField(
        widget=forms.DateTimeInput(
            attrs={"min": tomorow, "value": tomorow, "type": "date"}
        ),
        required=True,
    )


    class Meta:
        model = Subscription
        input_type = "date"
        fields = ["subscriptionplan", "billing_date", "expires"]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        outlet_id = kwargs.pop("outlet_id")
        super(ActivateSubscriptionForm, self).__init__(*args, **kwargs)
        user_id = self.request.user.id

        subscriptionplan = SubscriptionPlan.objects.filter(is_active=True)
        subscriptionplans = [(i.id, i.name) for i in subscriptionplan]
        SUBPLAN = [("", "--------")] + subscriptionplans

        outlet = (Outlet.objects.get(id=outlet_id.id)).name

        self.fields["subscriptionplan"].choices = SUBPLAN
        self.fields["subscriptionplan"].label = "Subscription Plan"
        self.fields["outlet"].initial = outlet


class ActivateSubscriptionMultiForm(MultiModelForm):
    form_classes = {
        "activate_subscription_form": ActivateSubscriptionForm,
        "billing_form": ActivateBillingForm,
    }

    def get_form_args_kwargs(self, key, args, kwargs):
        fargs, fkwargs = super(ActivateSubscriptionMultiForm, self).get_form_args_kwargs(key, args, kwargs)
        fkwargs.update({
            'request': kwargs.get('request'),
            'outlet_id' : kwargs.get('outlet_id')
        })
        return fargs, fkwargs