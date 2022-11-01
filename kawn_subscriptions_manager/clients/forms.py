from django.forms import ModelForm
from django import forms
import requests
from phonenumber_field.formfields import PhoneNumberField

from .models import Outlet, Client, Province, City
from kawn_subscriptions_manager.signature import prov


class AddOutletForm(ModelForm):
    class Meta:
        model = Outlet
        fields = [
            "client",
            "name",
            "display_name",
            "phone",
            "address",
            "province",
            "city",
        ]

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
        CITY = [("", "--------")] + cities

        client = Client.objects.all()
        clients = [(i.id, i.name) for i in client]
        CLIENT = [("", "--------")] + clients

        self.fields["province"] = forms.ChoiceField(choices=PROV, label="Province")
        self.fields["city"] = forms.ChoiceField(choices=CITY, label="City")
        self.fields["client"].choices = CLIENT


class AddClientForm(ModelForm):
    class Meta:
        model = Client
        fields = "__all__"
        exclude = ["user", "business_code", "brand_logo", "registered_via"]


class UpdateClientForm(ModelForm):
    class Meta:
        model = Client
        fields = "__all__"
        exclude = ["user", "business_code", "brand_logo", "registered_via"]


class AddClientOutletForm(ModelForm):
    class Meta:
        model = Outlet
        fields = ["name", "display_name", "phone", "address", "province", "city"]

    def __init__(self, *args, **kwargs):
        super(AddClientOutletForm, self).__init__(*args, **kwargs)
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
        CITY = [("", "--------")] + cities

        self.fields["province"] = forms.ChoiceField(choices=PROV, label="Province")
        self.fields["city"] = forms.ChoiceField(choices=CITY, label="City")
