import requests
import datetime
from httpsig.requests_auth import HTTPSignatureAuth
import environ

from kawn_subscriptions_manager.subscriptions.models  import SubscriptionPlan
from kawn_subscriptions_manager.signature import subscription_plans as sp


def post_subscription_plans():
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

  url = "https://" + DOMAIN + "/api/v2.1/internal-application/subscription-plan/"
  subplans = SubscriptionPlan.objects.all()
  subscription_plans = tuple(sp["results"])
  subplan_id = []
  for i in subscription_plans:
      subplan_id.append(
        i["id"]
      )

  payloads = []
  for subplan in subplans:
    if subplan.id not in subplan_id:
      payloads.append(
        {
          "name": subplan.name,
          "description": subplan.description,
          "price": subplan.price,
          "trial_period": subplan.trial_period,
          "trial_unit": subplan.trial_unit,
          "recurrence_period": subplan.recurrence_period,
          "recurrence_unit": subplan.recurrence_unit,
        }
      )

  if payloads:
    for payload in payloads:
      results = requests.post(url, auth=auth, headers=headers, json=payload, )

    if results.status_code == 201:
      print("Success")
    else:
      print(results.status_code)
  else:
    print("There is no new data to post")