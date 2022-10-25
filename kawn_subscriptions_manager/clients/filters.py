import django_filters

from .models import Outlet, Account
import django_filters as filters


class OutletFilter(django_filters.FilterSet):
    class Meta:
        model = Outlet
        fields = ["city_read", "province_read"]

    def __init__(self, *args, **kwargs):
        super(OutletFilter, self).__init__(*args, **kwargs)
        self.filters['city_read'].label="City"
        self.filters['city_read'].lookup_expr="icontains"
        self.filters['province_read'].label="Province"
        self.filters['province_read'].lookup_expr="icontains"

class AccountFilter(django_filters.FilterSet):
    class Meta:
        model = Account
        fields = ["name", "address"]

    def __init__(self, *args, **kwargs):
        super(AccountFilter, self).__init__(*args, **kwargs)
        self.filters['name'].label="Name"
        self.filters['name'].lookup_expr="icontains"
        self.filters['address'].label="Address"
        self.filters['address'].lookup_expr="icontains"
        
