from django.db import connection

from kawn_subscriptions_manager.signature import reqoutlet


data = tuple(reqoutlet["results"])

list_data = []
for edata in data:
        list_data.append(
            [
                edata["id"],
                edata["name"],
                edata["display_name"],
                edata["phone"],
                edata["address"],
                edata["postal_code"],
                edata["outlet_code"],
                edata["outlet_image"],
                edata["transaction_code_prefix"],
                edata["archieved"],
                edata["deleted"],
                edata["taxes"],
                edata["gratuity"],
                edata["enable_dashboard"],
                edata["branch_id"],
                edata["created"],
                edata["modified"],
                edata["province"],
                edata["city"],
            ]
        )


cursor = connection.cursor()
query = "INSERT INTO clients_outlet(id, name, display_name, phone, address, postal_code, outlet_code, outlet_image, transaction_code_prefix, archieved, deleted, taxes, gratuity, enable_dashboard, branch_id, created, modified, province, city) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING"
data = list_data
try:
    cursor.executemany(query, data)
    connection.commit()
    # print("Data outlet 1 stored to database")
except connection.DatabaseError as message:
    if connection:
        connection.rollback()
        print("Error occured", message)
finally:
    if cursor:
        cursor.close()
    if connection:
        connection.close()