import time
import requests
import hmac
import hashlib


class Const:
    SUMSUB_SECRET_KEY = "YOUR_SECRET_KEY"  # Example: Hej2ch71kG2kTd1iIUDZFNsO5C1lh5Gq
    SUMSUB_APP_TOKEN = "YOUR_APP_TOKEN"  # Example: tst:uY0CgwELmgUAEyl4hNWxLngb.0WSeQeiYny4WEqmAALEAiK2qTC96fBad
    SUMSUB_TEST_BASE_URL = "https://test-api.sumsub.com" # Please don't forget to change when switching to production

CONST = Const()

def getToken():
    global applicantId
    params = {"userId": 'USER_ID', "ttlInSecs": '600'}
    headers = {'Content-Type': 'application/json',
               'Content-Encoding': 'utf-8'
               }
    resp = sign_request(requests.Request('POST', CONST.SUMSUB_TEST_BASE_URL+'/resources/accessTokens',
                                         params=params,
                                         headers=headers
                                         ))
    s = requests.Session()
    ourresponse = s.send(resp)
    token = (ourresponse.json()['token'])
    print('Token:', token)



def sign_request(request: requests.Request) -> requests.PreparedRequest:
    prepared_request = request.prepare()
    now = int(time.time())
    method = request.method.upper()
    path_url = prepared_request.path_url  # includes encoded query params
    # could be None so we use an empty **byte** string here
    body = b'' if prepared_request.body is None else prepared_request.body
    if type(body) == str:
        body = body.encode('utf-8')
    data_to_sign = str(now).encode('utf-8') + method.encode('utf-8') + path_url.encode('utf-8') + body
    # hmac needs bytes
    signature = hmac.new(
        CONST.SUMSUB_SECRET_KEY.encode('utf-8'),
        data_to_sign,
        digestmod=hashlib.sha256
    )
    prepared_request.headers['X-App-Token'] = CONST.SUMSUB_APP_TOKEN
    prepared_request.headers['X-App-Access-Ts'] = str(now)
    prepared_request.headers['X-App-Access-Sig'] = signature.hexdigest()
    return prepared_request

getToken()

