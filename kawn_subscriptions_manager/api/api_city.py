from django.db import connection
from kawn_subscriptions_manager.signature import city, cities


data = cities
list_data = []
for edata in data:
    list_data.append(
        (
            edata["id"],
            edata["name"],
            edata["province"],
        )
    )

cursor = connection.cursor()
query = "INSERT INTO clients_city(id, name, province_id) VALUES(%s, %s, %s) ON CONFLICT DO NOTHING"
data = list_data
try:
    cursor.executemany(query, data)
    connection.commit()
    # print("Data city stored to database")
except connection.DatabaseError as message:
    if connection:
        connection.rollback()
        print("Error occured", message)
finally:
    if cursor:
        cursor.close()
    if connection:
        connection.close()