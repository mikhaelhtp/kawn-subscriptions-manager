from kawn_subscriptions_manager.signature import outlets, subscriptions
from kawn_subscriptions_manager.clients.models import Outlet


outlets_in_subscription = tuple(subscriptions["results"])
outlets = tuple(outlets["results"])

try:
    count = 0
    for outlet in outlets_in_subscription:
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
        count = count+1

    for outlet in outlets:
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
        count = count+1
    print(count,"outlet imported successfully.")
except:
    print("Error while importing outlet.")