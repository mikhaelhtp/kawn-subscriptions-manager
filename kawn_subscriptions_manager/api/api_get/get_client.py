from kawn_subscriptions_manager.signature import clients as c
from kawn_subscriptions_manager.clients.models import Client


def get_clients():
    clients = tuple(c["results"])

    try:
        count = 0
        for client in clients:
            Client.objects.bulk_create([
                Client(
                    id=client["id"],
                    name=client["name"],
                    address=client["address"], 
                    phone=client["phone"], 
                    business_code=client["business_code"],
                    brand_name=client["brand_name"],
                    brand_logo=client["brand_logo"],
                    social_facebook=client["social_facebook"],
                    social_twitter=client["social_twitter"],
                    social_instagram=client["social_instagram"],
                    website=client["website"],
                    registered_via=client["registered_via"]
                )
            ], ignore_conflicts=True)
            count = count+1
        print(count,"Client imported successfully.")
    except:
        print("Error while importing client.")