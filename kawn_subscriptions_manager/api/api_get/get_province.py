from kawn_subscriptions_manager.signature import provinces as p
from kawn_subscriptions_manager.clients.models import Province


def get_provinces():
    provinces = tuple(p["results"])

    try:
        count = 0
        for province in provinces:
            Province.objects.bulk_create([
                Province(id=province["id"], name=province["name"])
            ], ignore_conflicts=True)
            count = count+1
        print(count,"province imported successfully.")
    except:
        print("Error while importing province.")