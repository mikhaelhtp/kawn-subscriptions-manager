from kawn_subscriptions_manager.signature import cities,req
from kawn_subscriptions_manager.clients.models import (
    City,
)
from kawn_subscriptions_manager.subscriptions.models import (
    Subscription,
)

subscriptions = tuple(req["results"])

for city in cities:
    City.objects.bulk_create([
        City(id=city["id"], name=city["name"], province_id=city["province"])
    ], ignore_conflicts=True)

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