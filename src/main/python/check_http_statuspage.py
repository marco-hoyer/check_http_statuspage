#!/usr/bin/env python

import argparse

import requests
import sys

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


def exit_ok(message):
    print "OK - " + message
    sys.exit(0)


def exit_warning(message):
    print "WARNING - " + message
    sys.exit(1)


def exit_critical(message):
    print "CRITICAL - " + message
    sys.exit(2)


def exit_unknown(message):
    print "UNKNOWN - " + message
    sys.exit(3)


def get_url(protocol, host, port, uri):
    return "{0}://{1}:{2}{3}".format(protocol, host, port, uri)


def get_by_http(url):
    try:
        headers = {"accept": "application/json", "user-agent": "check_http_statuspage"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            if response.headers["content-type"] == "application/json":
                return response.json()
            else:
                exit_unknown("Server did not respond with 'content-type: application/json'")
        else:
            exit_unknown("Server responded with status-code: {0}".format(response.status_code))
            return None

    except Exception as e:
        exit_unknown(str(e))


def process_response(response_json):
    status = response_json["status"]
    message = response_json["message"]

    if str(status).lower() == "ok":
        exit_ok(message)
    if str(status).lower() == "warning":
        exit_warning(message)
    if str(status).lower() == "critical":
        exit_critical(message)
    if str(status).lower() == "unknown":
        exit_unknown(message)

    exit_unknown("Response status must be ok|warning|critical|unknown but was '{0}'".format(status))


def main(args):
    url = get_url(args.protocol, args.hostname, args.port, args.uri)
    process_response(get_by_http(url))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reads json from specified url and passes it as check result")
    parser.add_argument("protocol", help="protocol", type=str)
    parser.add_argument("hostname", help="hostname", type=str)
    parser.add_argument("port", help="port", type=int)
    parser.add_argument("uri", help="uri for resource to query (e.g. /internal)", type=str)
    args = parser.parse_args()
    main(args)
