from kawn_subscriptions_manager.signature import cities
from kawn_subscriptions_manager.clients.models import City


try:
    count = 0
    for city in cities:
        City.objects.bulk_create([
            City(id=city["id"], name=city["name"], province_id=city["province"])
        ], ignore_conflicts=True)
        count = count+1
    print(count,"city imported successfully.")
except:
    print("Error while importing city.")