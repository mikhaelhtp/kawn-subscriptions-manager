import math
import django_filters
from decimal import Decimal
from django.db.models import Q
from django.forms import TextInput
# from django_filters import FilterSet

from .models import User


class UserUniversalFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(
        method="universal_search",
        label="",
        widget=TextInput(attrs={"placeholder": "Search..."}),
    )

    class Meta:
        model = User
        fields = ["query"]

    def universal_search(self, queryset, name, value):
        if value.replace(".", "", 1).isdigit():
            value = Decimal(value)
            return User.objects.filter(Q(price=value) | Q(cost=value))

        return User.objects.filter(
            Q(name__icontains=value) | Q(category__icontains=value)
        )


class UserFilter(django_filters.FilterSet):
    id = django_filters.NumberFilter(label="")
    name = django_filters.CharFilter(label="", lookup_expr="istartswith")
    username = django_filters.CharFilter(label="", lookup_expr="istartswith")
    email = django_filters.NumberFilter(label="", method="filter_decimal")
    type = django_filters.NumberFilter(label="", method="filter_decimal")
    # status = django_filters.ChoiceFilter(label="", choices=User.Status.choices)

    class Meta:
        model = User
        fields = ["id", "name", "username", "email", "type"]

    def filter_decimal(self, queryset, name, value):
        # For price and cost, filter based on
        # the following property:
        # value <= result < floor(value) + 1

        lower_bound = "__".join([name, "gte"])
        upper_bound = "__".join([name, "lt"])

        upper_value = math.floor(value) + Decimal(1)

        return queryset.filter(**{lower_bound: value, upper_bound: upper_value})


# class UserFilter(FilterSet):
#     class Meta:
#         model = User
#         fields = {
#             "name": ["contains"],
#             "username": ["contains"],
#             "email": ["contains"],
#             "type": ["exact"],
#         }
