from kawn_subscriptions_manager.signature import subscription_plan
from kawn_subscriptions_manager.subscriptions.models import SubscriptionPlan


subscription_plans = tuple(subscription_plan["results"])

for subscriptionplan in subscription_plans:
    SubscriptionPlan.objects.bulk_create([
        SubscriptionPlan(
            id=subscriptionplan["id"],
            created=subscriptionplan["created"],
            modified=subscriptionplan["modified"],
            name=subscriptionplan["name"],
            description=subscriptionplan["description"],
            price=subscriptionplan["price"],
            trial_unit=subscriptionplan["trial_unit"],
            trial_period=subscriptionplan["trial_period"], 
            recurrence_unit=subscriptionplan["recurrence_unit"], 
            recurrence_period=subscriptionplan["recurrence_period"], 
            slug=subscriptionplan["slug"]
        )
    ], ignore_conflicts=True)