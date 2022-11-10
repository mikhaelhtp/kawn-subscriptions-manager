from django.db import connection
from kawn_subscriptions_manager.signature import prov


data = tuple(prov["results"])
list_data = []
for edata in data:
    list_data.append(
        (
            edata["id"],
            edata["name"],
        )
    )

cursor = connection.cursor()
query = "INSERT INTO clients_province(id, name) VALUES(%s, %s) ON CONFLICT DO NOTHING"
data = list_data
try:
    cursor.executemany(query, data)
    connection.commit()
    # print("Data province stored to database")
except connection.DatabaseError as message:
    if connection:
        connection.rollback()
        print("Error occured", message)
finally:
    if cursor:
        cursor.close()
    if connection:
        connection.close()