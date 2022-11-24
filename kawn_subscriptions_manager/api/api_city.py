from kawn_subscriptions_manager.signature import cities
from kawn_subscriptions_manager.clients.models import City


for city in cities:
    City.objects.bulk_create([
        City(id=city["id"], name=city["name"], province_id=city["province"])
    ], ignore_conflicts=True)