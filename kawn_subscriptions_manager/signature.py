import requests
import datetime
from httpsig.requests_auth import HTTPSignatureAuth
from kawn_subscriptions_manager.clients.models import Province
import environ

env = environ.Env()
environ.Env.read_env()

KAWN_SUBSCRIPTION_KEY_ID = env("KAWN_SUBSCRIPTION_KEY_ID")
KAWN_SUBSCRIPTION_SECRET = env("KAWN_SUBSCRIPTION_SECRET")
DOMAIN = "indev.kawn.co.id"

e = datetime.datetime.now()

signature_headers = ["(request-target)", "date"]
headers = {"Date": e.strftime("%a, %d %b %Y %I:%M:%S")}

auth = HTTPSignatureAuth(
    key_id=KAWN_SUBSCRIPTION_KEY_ID, secret=KAWN_SUBSCRIPTION_SECRET, algorithm="hmac-sha256", headers=signature_headers
)

subscriptions = requests.get(
    "https://"+ DOMAIN +"/api/v2.1/internal-application/subscription/?limit=1000",
    auth=auth,
    headers=headers,
).json()

outlets = requests.get(
    "https://"+ DOMAIN +"/api/v2.1/internal-application/outlet/?limit=1000",
    auth=auth,
    headers=headers,
).json()

provinces = requests.get(
    "https://"+ DOMAIN +"/api/v2.1/provinces/?ordering=id&limit=34&offset=0",
    auth=auth,
    headers=headers,
).json()

p = Province.objects.all().order_by("id")
cities = tuple()
for i in p:
    city = requests.get(
        "https://"+ DOMAIN +"/api/v2.1/provinces/"+ str(i.id) +"/cities/",
        auth=auth,
        headers=headers,
    ).json()
    cities += tuple(city["results"])

accounts = requests.get(
    "https://"+ DOMAIN +"/api/v2.1/account/",
    auth=auth,
    headers=headers,
).json()

subscription_plans = requests.get(
    "https://"+ DOMAIN +"/api/v2.1/internal-application/subscription-plan/",
    auth=auth,
    headers=headers,
).json()
