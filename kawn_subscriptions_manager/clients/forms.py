from django.forms import ModelForm
from django import forms

from .models import Outlet, Client, Province, City
from kawn_subscriptions_manager.users.models import User


class OutletForm(ModelForm):
    class Meta:
        model = Outlet
        fields = [
            "client",
            "name",
            "display_name",
            "phone",
            "address",
            "postal_code",
            "province",
            "city",
            "outlet_code",
            "transaction_code_prefix",
            "taxes", 
            "gratuity",
        ]

    def __init__(self, user, *args, **kwargs):
        super(OutletForm, self).__init__(*args, **kwargs)
        if user.type == "SALES":
            client = Client.objects.filter(user_id=user.id).order_by('name')
        else:
            client = Client.objects.all().order_by('name')
        clients = [(i.id, i.name) for i in client]
        CLIENT = [("", "--------")] + clients

        self.fields["city"].queryset = City.objects.none()
        if "province" in self.data:
            try:
                province_id = int(self.data.get("province"))
                self.fields["city"].queryset = City.objects.filter(
                    province_id=province_id
                ).order_by("name")
            except (ValueError, TypeError):
                pass

        province = Province.objects.all()
        provinces = [(i.id, i.name) for i in province]
        PROV = [("", "--------")] + provinces

        city = City.objects.all()
        cities = [(i.id, i.name) for i in city]
        CITY = [("", "--------")] + cities

        self.fields["province"] = forms.ChoiceField(choices=PROV, label="Province")
        self.fields["city"] = forms.ChoiceField(choices=CITY, label="City")
        self.fields["client"].choices = CLIENT


class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = ["user"]

    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)

        user = User.objects.filter(type="SALES")
        users = [(i.id, i.name) for i in user]
        USER = [("", "--------")] + users

        self.fields["user"].choices = USER
        self.fields["user"].label = "Sales Name"


class OutletClientForm(ModelForm):
    class Meta:
        model = Outlet
        fields = [
            "name",
            "display_name",
            "phone",
            "address",
            "postal_code",
            "province",
            "city",
            "outlet_code",
            "transaction_code_prefix",
            "taxes", 
            "gratuity",
            ]


    def __init__(self, *args, **kwargs):
        super(OutletClientForm, self).__init__(*args, **kwargs)
        self.fields["city"].queryset = City.objects.none()

        if "province" in self.data:
            try:
                province_id = int(self.data.get("province"))
                self.fields["city"].queryset = City.objects.filter(
                    province_id=province_id
                ).order_by("name")
            except (ValueError, TypeError):
                pass

        province = Province.objects.all()
        provinces = [(i.id, i.name) for i in province]
        PROV = [("", "--------")] + provinces

        city = City.objects.all()
        cities = [(i.id, i.name) for i in city]
        CITY = [("", "--------")] + cities

        self.fields["province"] = forms.ChoiceField(choices=PROV, label="Province")
        self.fields["city"] = forms.ChoiceField(choices=CITY, label="City")
