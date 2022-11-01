from django_filters import DateFilter, ChoiceFilter
import django_filters

from .models import (
    SubscriptionPlan,
    Subscription,
)


class SubscriptionPlanFilter(django_filters.FilterSet):
    STATUS_CHOICES = (
        (0, "Not Active"),
        (1, "Active"),
    )

    is_active = ChoiceFilter(choices=STATUS_CHOICES, label="Status:", empty_label="All")

    class Meta:
        model = SubscriptionPlan
        fields = ["trial_unit", "recurrence_unit"]

    def __init__(self, *args, **kwargs):
        super(SubscriptionPlanFilter, self).__init__(*args, **kwargs)
        self.filters["trial_unit"].label = "Trial Unit:"
        self.filters["trial_unit"].lookup_expr = "icontains"
        self.filters["recurrence_unit"].label = "Recurrence Unit:"
        self.filters["recurrence_unit"].lookup_expr = "icontains"


class SubscriptionFilter(django_filters.FilterSet):
    STATUS_CHOICES = (
        (0, "Not Active"),
        (1, "Active"),
    )

    active = ChoiceFilter(choices=STATUS_CHOICES, label="Status:", empty_label="All")
    subscriptionplan = ChoiceFilter(
        label="Subscription Plan:", empty_label="All", choices=[]
    )
    expires = DateFilter(
        field_name="expires", lookup_expr="lte", label="Exp Date Less Than:"
    )

    class Meta:
        model = Subscription
        fields = ["subscriptionplan", "outlet"]

    def __init__(self, *args, **kwargs):
        super(SubscriptionFilter, self).__init__(*args, **kwargs)
        subscription_plan = SubscriptionPlan.objects.all()
        subscription_plans = [(i.id, i.name) for i in subscription_plan]
        self.filters["subscriptionplan"].extra["choices"] = subscription_plans
        self.filters["outlet"].lookup_expr = "icontains"
