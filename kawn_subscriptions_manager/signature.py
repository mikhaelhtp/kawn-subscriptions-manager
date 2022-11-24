import requests
import datetime
from httpsig.requests_auth import HTTPSignatureAuth
from kawn_subscriptions_manager.clients.models import Province
import environ

env = environ.Env()
environ.Env.read_env()

KEY_ID = env("KEY_ID")
SECRET = env("SECRET")
DOMAIN = "indev.kawn.co.id"

e = datetime.datetime.now()

signature_headers = ["(request-target)", "date"]
headers = {"Date": e.strftime("%a, %d %b %Y %I:%M:%S")}

auth = HTTPSignatureAuth(
    key_id=KEY_ID, secret=SECRET, algorithm="hmac-sha256", headers=signature_headers
)

req = requests.get(
    "https://"+ DOMAIN +"/api/v2.1/internal-application/subscription/",
    auth=auth,
    headers=headers,
).json()

reqoutlet = requests.get(
    "https://"+ DOMAIN +"/api/v2.1/internal-application/outlet/",
    auth=auth,
    headers=headers,
).json()

prov = requests.get(
    "https://"+ DOMAIN +"/api/v2.1/provinces/",
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

account = requests.get(
    "https://"+ DOMAIN +"/api/v2.1/account/",
    auth=auth,
    headers=headers,
).json()

subscription_plan = requests.get(
    "https://"+ DOMAIN +"/api/v2.1/internal-application/subscription-plan/",
    auth=auth,
    headers=headers,
).json()
