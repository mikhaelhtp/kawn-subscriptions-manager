import django_filters

from .models import Outlet, Client


class OutletFilter(django_filters.FilterSet):
    class Meta:
        model = Outlet
        fields = ["name", "city_read", "province_read"]

    def __init__(self, *args, **kwargs):
        super(OutletFilter, self).__init__(*args, **kwargs)
        self.filters["name"].label = "Outlet Name"
        self.filters["name"].lookup_expr = "icontains"
        self.filters["city_read"].label = "City:"
        self.filters["city_read"].lookup_expr = "icontains"
        self.filters["province_read"].label = "Province:"
        self.filters["province_read"].lookup_expr = "icontains"


class ClientFilter(django_filters.FilterSet):
    class Meta:
        model = Client
        fields = ["name", "address"]

    def __init__(self, *args, **kwargs):
        super(ClientFilter, self).__init__(*args, **kwargs)
        self.filters["name"].label = "Name:"
        self.filters["name"].lookup_expr = "icontains"
        self.filters["address"].label = "Address:"
        self.filters["address"].lookup_expr = "icontains"
