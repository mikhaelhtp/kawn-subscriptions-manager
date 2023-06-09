from kawn_subscriptions_manager.signature import subscriptions as s
from kawn_subscriptions_manager.subscriptions.models import Subscription


def get_subscriptions():
    subscriptions = tuple(s["results"])

    try:
        count = 0
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
            count = count+1
        print(count,"subscription imported successfully.")
    except:
        print("Error while importing subscription.")