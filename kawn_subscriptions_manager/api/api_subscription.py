from kawn_subscriptions_manager.signature import subscriptions
from kawn_subscriptions_manager.subscriptions.models import Subscription


subscriptions = tuple(subscription["results"])

for subscription in subscriptions:
    Subscription.objects.bulk_create([
        Subscription(
            id=subscription["id"], 
            outlet_id=subscription["outlet"]["id"], 
            subscriptionplan_id=subscription["subscription_plan"]["id"], 
            expires=subscription["expires"], 
            billing_date=subscription["billing_date"], 
            active=subscription["active"], 
            cancelled=subscription["cancelled"], 
            voucher=subscription["voucher"], 
            created=subscription["created"], 
            deleted=subscription["deleted"], 
            modified=subscription["modified"])
    ], ignore_conflicts=True)