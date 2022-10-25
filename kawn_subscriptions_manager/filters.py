from random import choices
from django_filters import DateFilter
import django_filters

from kawn_subscriptions_manager.subscriptions.models import (
    SubscriptionPlan,
    Subscription,
)


class SubscriptionPlanFilter(django_filters.FilterSet):
    class Meta:
        model = SubscriptionPlan
        fields = ["name"]

    def __init__(self, *args, **kwargs):
        super(SubscriptionPlanFilter, self).__init__(*args, **kwargs)
        self.filters["name"].label = "Name"
        self.filters["name"].lookup_expr = "icontains"


class SubscriptionFilter(django_filters.FilterSet):

    expires = DateFilter(field_name="expires", lookup_expr="lte", label="Expired Date")

    class Meta:
        model = Subscription
        fields = ["active", "subscriptionplan"]

    def __init__(self, *args, **kwargs):
        super(SubscriptionFilter, self).__init__(*args, **kwargs)
        subscription_plan = SubscriptionPlan.objects.all()
        subscription_plans = [(i.id, i.name) for i in subscription_plan]
        self.filters["subscriptionplan"] = django_filters.ChoiceFilter(
            choices=subscription_plans
        )
        self.filters["active"].label = "Status"
        self.filters["active"].lookup_expr = "icontains"
