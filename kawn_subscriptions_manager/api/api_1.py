from kawn_subscriptions_manager.signature import prov, reqoutlet, req, subscription_plan
from kawn_subscriptions_manager.clients.models import (
    Province,
    Outlet
)
from kawn_subscriptions_manager.subscriptions.models import (
    SubscriptionPlan
)


provinces = tuple(prov["results"])
outlets1 = tuple(req["results"])
outlets2 = tuple(reqoutlet["results"])
subscription_plans = tuple(subscription_plan["results"])

for province in provinces:
    Province.objects.bulk_create([
        Province(id=province["id"], name=province["name"])
    ], ignore_conflicts=True)

for outlet in outlets1:
    if outlet["outlet"]["province"] is not None and outlet["outlet"]["city"] is not None:
        Outlet.objects.bulk_create([
            Outlet(
                id=outlet["outlet"]["id"], 
                name=outlet["outlet"]["name"], 
                display_name=outlet["outlet"]["display_name"], 
                subscription_plan_read=outlet["outlet"]["subscription_plan_read"], 
                phone=outlet["outlet"]["phone"], 
                province_read=outlet["outlet"]["province_read"], 
                city_read=outlet["outlet"]["city_read"], 
                address=outlet["outlet"]["address"], 
                postal_code=outlet["outlet"]["postal_code"], 
                outlet_code=outlet["outlet"]["outlet_code"], 
                outlet_image=outlet["outlet"]["outlet_image"], 
                is_expired=outlet["outlet"]["is_expired"], 
                transaction_code_prefix=outlet["outlet"]["transaction_code_prefix"], 
                archieved=outlet["outlet"]["archieved"], 
                deleted=outlet["outlet"]["deleted"], 
                taxes=outlet["outlet"]["taxes"], 
                gratuity=outlet["outlet"]["gratuity"], 
                enable_dashboard=outlet["outlet"]["enable_dashboard"], 
                branch_id=outlet["outlet"]["branch_id"],  
                device_users=outlet["outlet"]["device_users"],  
                created=outlet["outlet"]["created"], 
                modified=outlet["outlet"]["modified"],)
        ], ignore_conflicts=True)
    else:
        Outlet.objects.bulk_create([
            Outlet(
                id=outlet["outlet"]["id"], 
                name=outlet["outlet"]["name"], 
                display_name=outlet["outlet"]["display_name"], 
                subscription_plan_read=outlet["outlet"]["subscription_plan_read"], 
                phone=outlet["outlet"]["phone"], 
                province_read=outlet["outlet"]["province"], 
                city_read=outlet["outlet"]["city"], 
                address=outlet["outlet"]["address"], 
                postal_code=outlet["outlet"]["postal_code"], 
                outlet_code=outlet["outlet"]["outlet_code"], 
                outlet_image=outlet["outlet"]["outlet_image"], 
                is_expired=outlet["outlet"]["is_expired"], 
                transaction_code_prefix=outlet["outlet"]["transaction_code_prefix"], 
                archieved=outlet["outlet"]["archieved"], 
                deleted=outlet["outlet"]["deleted"], 
                taxes=outlet["outlet"]["taxes"], 
                gratuity=outlet["outlet"]["gratuity"], 
                enable_dashboard=outlet["outlet"]["enable_dashboard"], 
                branch_id=outlet["outlet"]["branch_id"],  
                device_users=outlet["outlet"]["device_users"],  
                created=outlet["outlet"]["created"], 
                modified=outlet["outlet"]["modified"],)
        ], ignore_conflicts=True)

for outlet in outlets2:
        Outlet.objects.bulk_create([
            Outlet(
                id=outlet["id"],
                name=outlet["name"],
                display_name=outlet["display_name"],
                phone=outlet["phone"],
                address=outlet["address"],
                postal_code=outlet["postal_code"],
                outlet_code=outlet["outlet_code"],
                outlet_image=outlet["outlet_image"],
                transaction_code_prefix=outlet["transaction_code_prefix"],
                archieved=outlet["archieved"],
                deleted=outlet["deleted"],
                taxes=outlet["taxes"],
                gratuity=outlet["gratuity"],
                enable_dashboard=outlet["enable_dashboard"],
                branch_id=outlet["branch_id"],
                created=outlet["created"],
                modified=outlet["modified"],
                province=outlet["province"],
                city=outlet["city"],
            )
        ], ignore_conflicts=True)

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