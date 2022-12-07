import datetime
import requests
import simplejson as json
from json import dumps
from httpsig.requests_auth import HTTPSignatureAuth
import environ

from kawn_subscriptions_manager.subscriptions.models import Subscription
from kawn_subscriptions_manager.signature import outlets

env = environ.Env()
environ.Env.read_env()

KAWN_SUBSCRIPTION_KEY_ID = env("KAWN_SUBSCRIPTION_KEY_ID")
KAWN_SUBSCRIPTION_SECRET = env("KAWN_SUBSCRIPTION_SECRET")
DOMAIN = "indev.kawn.co.id"

e = datetime.datetime.now()

signature_headers = ["(request-target)", "date"]
headers = {"Date": e.strftime("%a, %d %b %Y %I:%M:%S")}

auth = HTTPSignatureAuth(
    key_id=KAWN_SUBSCRIPTION_KEY_ID,
    secret=KAWN_SUBSCRIPTION_SECRET,
    algorithm="hmac-sha256",
    headers=signature_headers,
)

url = "https://" + DOMAIN + "/api/v2.1/internal-application/outlet/"
subscriptions = Subscription.objects.all()
outlets = tuple(outlets["results"])
outlet_id = []
for i in outlets:
    outlet_id.append(i["id"])

payloads = []
for subscription in subscriptions:
    if subscription.outlet_id not in outlet_id:
        payloads.append(
            {
                "subscription": {
                            "subscription_plan": subscription.subscriptionplan.id,
                            "billing": {
                                "subscription_detail": {
                                    "price": str(float(subscription.billing.price)),
                                    "current_plan": subscription.billing.subscriptiondetail.current_plan,
                                    "choosen_plan": subscription.billing.subscriptiondetail.choosen_plan
                                },
                                "order_payment": {
                                    "code": str(subscription.billing.orderpayment.code),
                                    "status": subscription.billing.orderpayment.status,
                                    "payment_type": subscription.billing.orderpayment.payment_type,
                                    "amount": str(
                                        float(subscription.billing.orderpayment.amount)
                                    )
                                },
                                "price": str(float(subscription.billing.price)),
                                "due_date": str((subscription.billing_date).date())
                            },
                            "expired_date": str((subscription.expires).date()),
                            "expires": str((subscription.expires).date()),
                            "billing_date": str((subscription.billing_date).date()),
                            "active": subscription.active,
                            "cancelled": subscription.cancelled,
                        },
                        "name": subscription.outlet.name,
                        "display_name": subscription.outlet.display_name,
                        "transaction_code_prefix": subscription.outlet.transaction_code_prefix,
                        "phone": "0" + str(subscription.outlet.phone.national_number),
                        "address": subscription.outlet.address,
                        "postal_code": subscription.outlet.postal_code,
                        "outlet_code": subscription.outlet.outlet_code,
                        "taxes": subscription.outlet.taxes,
                        "gratuity": subscription.outlet.gratuity,
                        "archieved": subscription.outlet.archieved,
                        "enable_dashboard": subscription.outlet.enable_dashboard,
                        "account": subscription.outlet.client_id,
                        "province": subscription.outlet.province,
                        "city": subscription.outlet.city
            })

for payload in payloads:
    results = requests.post(url, auth=auth, headers=headers, json=payload)

if results.status_code == 201:
    print("Success Post Data")
else:
    print(results.status_code)
    print(results.reason)
