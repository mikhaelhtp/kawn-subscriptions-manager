from django.forms import ModelForm
from django import forms
import requests
from phonenumber_field.formfields import PhoneNumberField

from .models import Outlet, Account
from kawn_subscriptions_manager.signature import prov


class AddOutletForm(ModelForm):
    class Meta:
        model = Outlet
        fields = ["name", "display_name", "phone", "province", "address"]

    def __init__(self, *args, **kwargs):
        super(AddOutletForm, self).__init__(*args, **kwargs)
        province = tuple(prov["results"])
        provinces = [(i["id"], i["name"]) for i in province]

        self.fields["province"] = forms.ChoiceField(choices=provinces, label="Province")
        self.fields['display_name'].required = False


class AddClientForm(ModelForm):
    class Meta:
        model = Account
        fields = "__all__"
        exclude = ["user", "business_code", "brand_logo"]
        # exclude = ["branch_id", "subscription_plan_read", "province_read", "outlet_code", "outlet_image", "is_expired", "transaction_code_prefix", "account_id"]

    # def __init__(self, *args, **kwargs):
    #     super(AddClientForm, self).__init__(*args, **kwargs)

    #     self.fields["phone"] = PhoneNumberField()


class UpdateClientForm(ModelForm):
    class Meta:
        model = Account
        fields = "__all__"
        exclude = ["user", "business_code", "brand_logo"]


class AddClientOutletForm(ModelForm):
    class Meta:
        model = Outlet
        fields = ["name"]

    def __init__(self, *args, **kwargs):
        super(AddClientOutletForm, self).__init__(*args, **kwargs)

        outlet = Outlet.objects.filter(account_id__isnull=True)
        outlets = [(i.id, i.name) for i in outlet]

        self.fields["name"] = forms.ChoiceField(choices=outlets, label="Choose Outlet")
