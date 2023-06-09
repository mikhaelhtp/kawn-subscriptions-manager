import requests
import datetime
from httpsig.requests_auth import HTTPSignatureAuth
import environ

from kawn_subscriptions_manager.subscriptions.models import SubscriptionPlan


def put_subscription_plans():
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

  subplans = SubscriptionPlan.objects.all()
  id = []
  for i in subplans:
    id.append(
      i.id
    )

  for i in id:
    url = "https://" + DOMAIN + "/api/v2.1/internal-application/subscription-plan/"+ str(i) +"/"

  payloads = []
  for subplan in subplans:
      payloads.append(
        {
          "id": subplan.id,
          "name": subplan.name,
          "description": subplan.description,
          "price": str(float(subplan.price)),
          "trial_period": subplan.trial_period,
          "trial_unit": subplan.trial_unit,
          "recurrence_period": subplan.recurrence_period,
          "recurrence_unit": subplan.recurrence_unit,
          "slug": subplan.slug,
        }
      )

  if payloads:
    for payload in payloads:
      results = requests.put(url, auth=auth, headers=headers, json=payload)

    if results.status_code == 200:
      print("Success update subscription plans")
    else:
      print(results.status_code)
  else:
    print("There is no subscription plans to put")