import requests
import datetime
from httpsig.requests_auth import HTTPSignatureAuth
import environ

from kawn_subscriptions_manager.subscriptions.models import Subscription
from kawn_subscriptions_manager.signature import outlets as o


def put_subscriptions():
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

    subscriptions = Subscription.objects.all()
    
    outlet = tuple(o["results"])
    outlet_id = []
    for i in outlet:
      outlet_id.append(i["id"])

    id = []
    for subs in subscriptions:
        if subs.billing_id:
            id.append(subs.id)

    for i in id:
        url = (
            "https://"
            + DOMAIN
            + "/api/v2.1/internal-application/subscription/"
            + str(i)
            + "/"
        )

    payloads = []
    for subscription in subscriptions:
        if subscription.outlet.id in outlet_id and subscription.billing:
            payloads.append(
                {
                    "outlet": {
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
                        "province": subscription.outlet.province,
                        "city": subscription.outlet.city,
                    },
                    "subscription_plan": {
                        "name": subscription.subscriptionplan.name,
                        "description": subscription.subscriptionplan.description,
                        "price": str(float(subscription.subscriptionplan.price)),
                        "trial_period": subscription.subscriptionplan.trial_period,
                        "trial_unit": subscription.subscriptionplan.trial_unit,
                        "recurrence_period": subscription.subscriptionplan.recurrence_period,
                        "recurrence_unit": subscription.subscriptionplan.recurrence_unit,
                    },
                    "billing": {
                        "subscription_detail": {
                            "price": str(float(subscription.billing.price)),
                            "current_plan": subscription.billing.subscriptiondetail.current_plan,
                            "choosen_plan": subscription.billing.subscriptiondetail.choosen_plan,
                        },
                        "order_payment": {
                            "code": str(subscription.billing.orderpayment.code),
                            "status": subscription.billing.orderpayment.status,
                            "method": "others",
                            "payment_type": subscription.billing.orderpayment.payment_type,
                            "amount": str(
                                float(subscription.billing.orderpayment.amount)
                            ),
                        },
                        "price": str(float(subscription.billing.price)),
                        "due_date": str((subscription.billing_date).date()),
                    },
                    "expired_date": str((subscription.expires).date()),
                    "expires": str((subscription.expires).date()),
                    "billing_date": str((subscription.billing_date).date()),
                    "active": subscription.active,
                    "cancelled": subscription.cancelled,
                }
            )

    if payloads:
        for payload in payloads:
            results = requests.put(url, json=payload, auth=auth, headers=headers)

        if results.status_code == 200:
            print("Success Updated Data")
        else:
            print(results.status_code)
    else:
        print("There is no new data to put.")
