from django.forms import ModelForm
from django import forms
import requests
from phonenumber_field.formfields import PhoneNumberField

from .models import Outlet, Account, Province, City
from kawn_subscriptions_manager.signature import prov


class AddOutletForm(ModelForm):
    class Meta:
        model = Outlet
        fields = ["name", "display_name", "phone", "province", "city", "address"]

    def __init__(self, *args, **kwargs):
        super(AddOutletForm, self).__init__(*args, **kwargs)
        self.fields["city"].queryset = City.objects.none()

        if "province" in self.data:
            try:
                province_id = int(self.data.get("province"))
                self.fields["city"].queryset = City.objects.filter(
                    province_id=province_id
                ).order_by("name")
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        # elif self.instance.pk:
        #     self.fields['city'].queryset = self.instance.province.city_set.order_by('name')

        province = Province.objects.all()
        provinces = [(i.id, i.name) for i in province]
        PROV = [("", "--------")] + provinces

        city = City.objects.all()
        cities = [(i.id, i.name) for i in city]
        CTY = [("", "--------")] + cities

        self.fields["province"] = forms.ChoiceField(choices=PROV, label="Province")
        self.fields["city"] = forms.ChoiceField(choices=CTY, label="City")


class AddClientForm(ModelForm):
    class Meta:
        model = Account
        fields = "__all__"
        exclude = ["user", "business_code", "brand_logo", "registered_via"]


class UpdateClientForm(ModelForm):
    class Meta:
        model = Account
        fields = "__all__"
        exclude = ["user", "business_code", "brand_logo", "registered_via"]


class AddClientOutletForm(ModelForm):
    class Meta:
        model = Outlet
        fields = ["name"]

    def __init__(self, *args, **kwargs):
        super(AddClientOutletForm, self).__init__(*args, **kwargs)

        outlet = Outlet.objects.filter(account_id__isnull=True)
        outlets = [(i.id, i.name) for i in outlet]

        self.fields["name"] = forms.ChoiceField(choices=outlets, label="Choose Outlet")
