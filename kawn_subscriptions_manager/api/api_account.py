from django.db import connection
from kawn_subscriptions_manager.signature import account


data = tuple(account)
list_data = []
for edata in data:
    list_data.append(
        (
            edata["id"],
            edata["created"],
            edata["modified"],
            edata["name"],
            edata["address"],
            edata["phone"],
            edata["business_code"],
            edata["brand_name"],
            edata["brand_logo"],
            edata["social_facebook"],
            edata["social_twitter"],
            edata["social_instagram"],
            edata["website"],
            edata["registered_via"],
        )
    )

cursor = connection.cursor()
query = "INSERT INTO clients_account(id, created, modified, name, address, phone, business_code, brand_name, brand_logo, social_facebook, social_twitter, social_instagram, website, registered_via) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING"
data = list_data
try:
    cursor.executemany(query, data)
    connection.commit()
    # print("Data account stored to database")
except connection.DatabaseError as message:
    if connection:
        connection.rollback()
        print("Error occured", message)
finally:
    if cursor:
        cursor.close()
    if connection:
        connection.close()