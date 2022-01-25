import logging

import azure.functions as func
from datetime import datetime
from time import mktime
import uuid
import hmac
import requests
import json
from hashlib import sha256
import optparse
import time
import sys

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    req_body = req.get_json()
    logging.info(str(req_body))
    if(req_body[0]['IsSpikeAndDipAnomaly']==1):
        logging.info('Anomaly detected: STOP mining')
        try:
            host = "https://api2.nicehash.com"
            key = "3e2d28e3-55b0-4b7c-8177-712c66edbeec"
            secret = "38764557-06f6-429c-b89a-2b744fd4044b3c8d7267-1182-48a2-81c8-5ea70d5906c9"
            organisation_id = "c087342f-088b-48bb-b0a9-61d380e97f65"
            verbose = False
            method = "POST"
            path = "/main/api/v2/mining/rigs/status2"
            query = ''
            body = {"action":"STOP","rigId":"0-r4BbTFKXYFWXTRFBFwuE9Q"}

            now = datetime.now()
            now_ec_since_epoch = mktime(now.timetuple()) + now.microsecond / 1000000.0
            xtime = int(now_ec_since_epoch * 1000)

            xnonce = str(uuid.uuid4())

            message = bytearray(key, 'utf-8')
            message += bytearray('\x00', 'utf-8')
            message += bytearray(str(xtime), 'utf-8')
            message += bytearray('\x00', 'utf-8')
            message += bytearray(xnonce, 'utf-8')
            message += bytearray('\x00', 'utf-8')
            message += bytearray('\x00', 'utf-8')
            message += bytearray(organisation_id, 'utf-8')
            message += bytearray('\x00', 'utf-8')
            message += bytearray('\x00', 'utf-8')
            message += bytearray(method, 'utf-8')
            message += bytearray('\x00', 'utf-8')
            message += bytearray(path, 'utf-8')
            message += bytearray('\x00', 'utf-8')
            message += bytearray(query, 'utf-8')
            
            body_json = json.dumps(body)
            message += bytearray('\x00', 'utf-8')
            message += bytearray(body_json, 'utf-8')

            digest = hmac.new(bytearray(secret, 'utf-8'), message, sha256).hexdigest()
            xauth = key + ":" + digest

            headers = {
                'X-Time': str(xtime),
                'X-Nonce': xnonce,
                'X-Auth': xauth,
                'Content-Type': 'application/json',
                'X-Organization-Id': organisation_id,
                'X-Request-Id': str(uuid.uuid4())
            }

            s = requests.Session()
            s.headers = headers

            url = host + path

            response = s.request(method, url, data=body_json)
            response = response.json()
            logging.info(str(response))
            logging.info('STOP Success')

        except Exception as ex:
            logging.info(str(ex))

    else:
        logging.info('No Anomaly')
    return func.HttpResponse(f"OK")


    