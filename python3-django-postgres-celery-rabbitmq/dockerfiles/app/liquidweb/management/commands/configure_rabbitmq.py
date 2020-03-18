import base64
import json
import time
from urllib.parse import urlparse

from amqp import exceptions as amqp_exc
from django.conf import settings
from django.core.management import BaseCommand
import kombu
import requests
from requests.packages.urllib3.util import retry as requests_retry


def verify_rmq_access():  # pragma: no cover
    amqp_url = settings.RMQ_AMQP_CONNECTION_STRING
    with kombu.Connection(amqp_url) as rmq_connection:
        attempts = 0
        max_attempts = 100
        while attempts < max_attempts:
            try:
                rmq_connection.connect()
                return rmq_connection.connected
            except amqp_exc.NotAllowed:
                return False
            except IOError as exc:
                print("RabbitMQ connection error; retrying..")
                time.sleep(10)
                attempts += 1
                if attempts >= max_attempts:
                    raise exc



def reconcile_rmq_vhost():  # pragma: no cover
    url = settings.RMQ_API_ENDPOINT
    vhost_name = settings.RMQ_VHOST
    user = settings.RMQ_USER
    userPass = user + ":" + settings.RMQ_PASSWORD
    authHeader = "Basic " + base64.b64encode(userPass.encode()).decode("utf-8")
    payload = json.dumps({"vhosts": [ { "name": vhost_name } ],
                          "permissions": [ { "user": user, "vhost": vhost_name, "configure": ".*", "write": ".*", "read": ".*"}],
                          "policies": [ { "vhost": vhost_name, "name": "sync-nodes-" + vhost_name, "pattern": ".*", "apply-to": "all",
                                          "definition": { "ha-sync-mode": "automatic", "ha-mode": "all" }, "priority": 0} ]
                          })

    headers = {
        'authorization': authHeader,
        'content-type': "application/json",
    }

    requests_session = requests.Session()

    parsed_url = urlparse(url)
    retry_adapter = requests.adapters.HTTPAdapter(
        max_retries=requests_retry.Retry(
            total=400,
            backoff_factor=0.5,
            method_whitelist=set(['POST']),
        )
    )
    requests_session.mount('{scheme}://'.format(scheme=parsed_url.scheme), retry_adapter)
    response = requests_session.request("POST", url, data=payload, headers=headers)
    if response.ok:
        print('Created vhost and permissions for: {vhost}'.format(vhost=vhost_name))
    else:
        print("Could not create vhost {vhost} on RabbitMQ management API endpoint {api_endpoint}: {reason}".format(vhost=vhost_name, api_endpoint=url, reason=response.reason))
        response.raise_for_status()


class Command(BaseCommand):
    help = 'Ensures RabbitMQ is configured correctly'

    def handle(self, *args, **kwargs): # pragma: no cover
        if not verify_rmq_access():
            print("No access to the RabbitMQ vhost with provided credentials; attempting to reconcile..")
            reconcile_rmq_vhost()
