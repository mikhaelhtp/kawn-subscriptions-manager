from django.db import connection
from kawn_subscriptions_manager.signature import req


data = tuple(req["results"])

list_data = []
for edata in data:
    list_data.append(
        (
            edata["id"],
            edata["outlet"]["id"],
            edata["subscription_plan"]["id"],
            edata["expires"],
            edata["billing_date"],
            edata["active"],
            edata["cancelled"],
            edata["voucher"],
            edata["created"],
            edata["deleted"],
            edata["modified"],
        )
    )

cursor = connection.cursor()
query = "INSERT INTO subscriptions_subscription(id, outlet_id, subscriptionplan_id, expires, billing_date, active, cancelled, voucher, created, deleted, modified) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING"
data = list_data
try:
    cursor.executemany(query, data)
    connection.commit()
    # print("Data subscriptions stored to database")
except connection.DatabaseError as message:
    if connection:
        connection.rollback()
        print("Error occured", message)
finally:
    if cursor:
        cursor.close()
    if connection:
        connection.close()     