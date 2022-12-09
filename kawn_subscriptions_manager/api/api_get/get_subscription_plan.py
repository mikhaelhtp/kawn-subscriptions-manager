from kawn_subscriptions_manager.signature import subscription_plans as sp
from kawn_subscriptions_manager.subscriptions.models import SubscriptionPlan


def get_subscription_plans():
    subscription_plans = tuple(sp["results"])

    try:
        count = 0
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
            count = count+1
        print(count,"subscription plan imported successfully.")
    except:
        print("Error while importing subscription plan.")