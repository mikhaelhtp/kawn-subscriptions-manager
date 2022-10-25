from django.db import connection

from kawn_subscriptions_manager.signature import req


data = tuple(req["results"])

list_data = []
for edata in data:
    if edata["outlet"]["province"] is not None and edata["outlet"]["city"] is not None:
        list_data.append(
            [
                edata["outlet"]["id"],
                edata["outlet"]["name"],
                edata["outlet"]["display_name"],
                edata["outlet"]["subscription_plan_read"],
                edata["outlet"]["phone"],
                edata["outlet"]["province_read"],
                edata["outlet"]["city_read"],
                edata["outlet"]["address"],
                edata["outlet"]["postal_code"],
                edata["outlet"]["outlet_code"],
                edata["outlet"]["outlet_image"],
                edata["outlet"]["is_expired"],
                edata["outlet"]["transaction_code_prefix"],
                edata["outlet"]["archieved"],
                edata["outlet"]["deleted"],
                edata["outlet"]["taxes"],
                edata["outlet"]["gratuity"],
                edata["outlet"]["enable_dashboard"],
                edata["outlet"]["branch_id"],
                edata["outlet"]["device_users"],
                edata["outlet"]["created"],
                edata["outlet"]["modified"],
            ]
        )
    else:
        list_data.append(
            [
                edata["outlet"]["id"],
                edata["outlet"]["name"],
                edata["outlet"]["display_name"],
                edata["outlet"]["subscription_plan_read"],
                edata["outlet"]["phone"],
                edata["outlet"]["province"],
                edata["outlet"]["city"],
                edata["outlet"]["address"],
                edata["outlet"]["postal_code"],
                edata["outlet"]["outlet_code"],
                edata["outlet"]["outlet_image"],
                edata["outlet"]["is_expired"],
                edata["outlet"]["transaction_code_prefix"],
                edata["outlet"]["archieved"],
                edata["outlet"]["deleted"],
                edata["outlet"]["taxes"],
                edata["outlet"]["gratuity"],
                edata["outlet"]["enable_dashboard"],
                edata["outlet"]["branch_id"],
                edata["outlet"]["device_users"],
                edata["outlet"]["created"],
                edata["outlet"]["modified"],
            ]
        )


cursor = connection.cursor()
query = "INSERT INTO clients_outlet(id, name, display_name, subscription_plan_read, phone, province_read, city_read, address, postal_code, outlet_code, outlet_image, is_expired, transaction_code_prefix, archieved, deleted, taxes, gratuity, enable_dashboard, branch_id, device_users, created, modified) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING"
data = list_data
try:
    cursor.executemany(query, data)
    connection.commit()
    print("Data outlet stored to database")
except connection.DatabaseError as message:
    if connection:
        connection.rollback()
        print("Error occured", message)
finally:
    if cursor:
        cursor.close()
    if connection:
        connection.close()