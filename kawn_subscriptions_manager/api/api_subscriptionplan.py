from django.db import connection
from django.utils.translation import gettext_lazy as _

from kawn_subscriptions_manager.signatures import req


data = tuple(req["results"])

list_data = []
for edata in data:
    list_data.append(
        (
            edata["subscription_plan"]["id"],
            edata["subscription_plan"]["created"],
            edata["subscription_plan"]["modified"],
            edata["subscription_plan"]["name"],
            edata["subscription_plan"]["description"],
            edata["subscription_plan"]["price"],
            edata["subscription_plan"]["trial_unit"],
            edata["subscription_plan"]["trial_period"],
            edata["subscription_plan"]["recurrence_unit"],
            edata["subscription_plan"]["recurrence_period"],
            edata["subscription_plan"]["slug"],
            edata["subscription_plan"]["is_public"],
            edata["subscription_plan"]["plan_type"],
        )
    )


cursor = connection.cursor()
query = (
    "INSERT INTO subscriptions_apisubscriptionplan(id, created, modified, name, description, price, trial_unit, trial_period, recurrence_unit, recurrence_period, slug, is_public, plan_type)"
    + "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    + "ON CONFLICT DO NOTHING"
)

data = list_data
try:
    cursor.executemany(query, data)
    connection.commit()
    # print("Data stored to database")
except connection.DatabaseError as message:
    if connection:
        connection.rollback()
        print("Error occured", message)
finally:
    if cursor:
        cursor.close()
    if connection:
        connection.close()
