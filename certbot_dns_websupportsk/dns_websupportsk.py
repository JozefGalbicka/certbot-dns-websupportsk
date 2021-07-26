# imports for WebsupportAPI class
import hmac
import hashlib
import time
import requests
import base64
from datetime import datetime, timezone
import json

# imports for authenticator
import json
import logging
import time

import requests
import zope.interface

from certbot import errors
from certbot import interfaces
from certbot.plugins import dns_common


@zope.interface.implementer(interfaces.IAuthenticator)
@zope.interface.provider(interfaces.IPluginFactory)
class Authenticator(dns_common.DNSAuthenticator):
    """DNS Authenticator for Websupport
    This Authenticator uses the Websupport Remote REST API to fulfill a dns-01 challenge.
    """

    description = "Obtain certificates using a DNS TXT record (if you are using Websupport for DNS)."
    ttl = 60

    def __init__(self, *args, **kwargs):
        super(Authenticator, self).__init__(*args, **kwargs)
        self.credentials = None

    @classmethod
    def add_parser_arguments(cls, add, **kwargs):  # pylint: disable=arguments-differ
        super(Authenticator, cls).add_parser_arguments(
            add, default_propagation_seconds=120
        )
        add("credentials", help="Websupport credentials INI file.")

    def more_info(self):  # pylint: disable=missing-docstring,no-self-use
        return (
            "This plugin configures a DNS TXT record to respond to a dns-01 challenge using "
            + "the Websupport Remote REST API."
        )

    def _setup_credentials(self):
        self.credentials = self._configure_credentials(
            "credentials",
            "Websupport credentials INI file",
            {
                "api_key": "API key for Websupport Remote API.",
                "secret": "Password for Websupport Remote API.",
                "domain": "Domain for dns01 authentication.",
            },
        )

    def _perform(self, domain, validation_name, validation):
        self._get_websupport_client().handle_wildcard_auth(validation_name, validation)

    def _cleanup(self, domain, validation_name, validation):
        self._get_websupport_client().clean_wildcard_auth(validation_name)

    def _get_websupport_client(self):
        return WebsupportAPI(
            self.credentials.conf("api_key"),
            self.credentials.conf("secret"),
            self.credentials.conf("domain"),
        )


def print_json_data(json_data):
    print(json.dumps(json_data, indent=2))


class WebsupportAPI:
    def __init__(self, api_key, secret, domain):
        self.default_path = "/v1/user/self"
        self.api = "https://rest.websupport.sk"
        self.query = ""  # query part is optional and may be empty
        self.domain = domain

        # creating signature
        method = "GET"
        timestamp = int(time.time())
        canonical_request = "%s %s %s" % (method, self.default_path, timestamp)
        signature = hmac.new(bytes(secret, 'UTF-8'), bytes(canonical_request, 'UTF-8'), hashlib.sha1).hexdigest()

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Date": datetime.fromtimestamp(timestamp, timezone.utc).isoformat()
        }

        # creating session
        self.s = requests.Session()
        self.s.auth = (api_key, signature)
        self.s.headers.update(headers)
        login_response = self.s.get("%s%s%s" % (self.api, self.default_path, self.query)).content

    def get_records(self, type_=None, id_=None, name=None, content=None, ttl=None, note=None):
        # create dict of arguments passed, filter out 'None' values and 'self' argument, rename keys(remove "_"
        # trailing)
        args = {k.replace("_", ""): v for k, v in locals().items() if v is not None and k != 'self'}
        # get data from api
        data = json.loads(self.s.get(f"{self.api}{self.default_path}/zone/{self.domain}/record{self.query}").content)
        items = data["items"]
        print(f"Getting records, arguments: {args},... found: {len(items)} item(s)")

        records = list()
        for item in items:
            shared_keys = args.keys() & item.keys()
            # intersection dict of shared items
            intersection_dict = {k: item[k] for k in shared_keys if item[k] == args[k]}
            # record is valid only if all values from args match
            records.append(item) if len(intersection_dict) == len(args) else None

        return records

    def create_record(self, type_, name, content, ttl=600, **kwargs):
        # print(get_records(type_=type_, name=name, content=content))

        args = {k.replace("_", ""): v for k, v in locals().items()}
        args.pop('self')
        args.pop('kwargs')
        args.update(**kwargs)
        print(f"Creating record: type:{type_}, name:{name}, content:{content}", end="    ")
        print(self.s.post(f"{self.api}{self.default_path}/zone/{self.domain}/record", json=args))

    def edit_record(self, id_, **kwargs):
        print(f"Editing record: id:{id_}, kwargs:{kwargs}", end="    ")
        print(self.s.put(f"{self.api}{self.default_path}/zone/{self.domain}/record/{id_}", json=kwargs))

    def delete_record(self, id_):
        print(f"Deleting record: id:{id_}, end="    ")
        print(self.s.delete(f"{self.api}{self.default_path}/zone/{self.domain}/record/{id_}"))

    # TO-DO: add error handling for not found record and multiple records found
    def get_record_id(self, type_, name, **kwargs):
        record = self.get_records(type_=type_, name=name, **kwargs)
        return record[0]['id'] if len(record) == 1 and type(record) == list else None

    def handle_wildcard_auth(self, subdomain, validation_token):
        id_ = self.get_record_id(type_="TXT", name=subdomain)

        if not id_:
            self.create_record(type_="TXT", name=subdomain, content=validation_token)
        else:
            self.edit_record(id_=id_, content=validation_token)

    def clean_wildcard_auth(self, subdomain):
        id_ = self.get_record_id("TXT", subdomain)
        self.delete_record(id_)

