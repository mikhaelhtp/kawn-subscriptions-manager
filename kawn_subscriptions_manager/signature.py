import requests
import datetime
from httpsig.requests_auth import HTTPSignatureAuth

KEY_ID = "a206c5980f385ba96ff3f1b5979986c0d11a058e"
SECRET = "33d1ac21bec6cae44c2d7bedcb521938b9b3d436"
e = datetime.datetime.now()

signature_headers = ["(request-target)", "date"]
headers = {"Date": e.strftime("%a, %d %b %Y %I:%M:%S")}

auth = HTTPSignatureAuth(
    key_id=KEY_ID, secret=SECRET, algorithm="hmac-sha256", headers=signature_headers
)

req = requests.get(
    "https://indev.kawn.co.id/api/v2.1/internal-application/subscription/",
    auth=auth,
    headers=headers,
).json()

reqoutlet = requests.get(
    "https://indev.kawn.co.id/api/v2.1/internal-application/outlet/",
    auth=auth,
    headers=headers,
).json()

prov = requests.get(
    "https://indev.kawn.co.id/api/v2.1/provinces/",
    auth=auth,
    headers=headers,
).json()

account = requests.get(
    "https://indev.kawn.co.id/api/v2.1/account/",
    auth=auth,
    headers=headers,
).json()

