from django.db import connection
from kawn_subscriptions_manager.signature import subscription_plan


data = tuple(subscription_plan["results"])
list_data = []
for edata in data:
    list_data.append(
        (
            edata["id"],
            edata["created"],
            edata["modified"],
            edata["name"],
            edata["description"],
            edata["price"],
            edata["trial_unit"],
            edata["trial_period"],
            edata["recurrence_unit"],
            edata["recurrence_period"],
            edata["slug"],
        )
    )

cursor = connection.cursor()
query = "INSERT INTO subscriptions_subscriptionplan(id, created, modified, name, description, price, trial_unit, trial_period, recurrence_unit, recurrence_period, slug) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING"
data = list_data
try:
    cursor.executemany(query, data)
    connection.commit()
    # print("Data subscriptions plan stored to database")
except connection.DatabaseError as message:
    if connection:
        connection.rollback()
        print("Error occured", message)
finally:
    if cursor:
        cursor.close()
    if connection:
        connection.close()