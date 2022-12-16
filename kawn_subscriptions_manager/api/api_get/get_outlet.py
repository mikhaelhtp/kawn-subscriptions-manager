from kawn_subscriptions_manager.signature import outlets as o
from kawn_subscriptions_manager.clients.models import Outlet


def get_outlets():
    outlets = tuple(o["results"])

    try:
        count = 0
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
                    created=outlet["created"],
                    modified=outlet["modified"],
                    province=outlet["province"],
                    city=outlet["city"],
                    client_id=outlet["account"],
                )
            ], ignore_conflicts=True)
            count = count+1
        print(count,"outlet imported successfully.")
    except:
        print("Error while importing outlet.")