from django.db import connection
from django.utils.translation import gettext_lazy as _

from kawn_subscriptions_manager.signatures import req


data = tuple(req["results"])

list_data = []
for edata in data:
    list_data.append(
        (
            edata["id"],
            edata["outlet"]["name"],
            edata["subscription_plan"]["name"],
            edata["deleted"],
            edata["created"],
            edata["modified"],
            edata["expires"],
            edata["billing_date"],
            edata["active"],
            edata["cancelled"],
            edata["voucher"],
        )
    )


cursor = connection.cursor()
query = (
    "INSERT INTO subscriptions_apisubscription(id, outlet_name, subscriptionplan_name, deleted, created, modified, expires, billing_date, active, cancelled, voucher)"
    + "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
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
