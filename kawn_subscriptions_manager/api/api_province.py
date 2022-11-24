from kawn_subscriptions_manager.signature import provinces
from kawn_subscriptions_manager.clients.models import Province


provinces = tuple(provinces["results"])

for province in provinces:
    Province.objects.bulk_create([
        Province(id=province["id"], name=province["name"])
    ], ignore_conflicts=True)