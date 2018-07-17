import json

import requests

PRODUCTION = False

PROD_URL = 'http://monit-metrics.cern.ch:10012'
DEV_URL = 'http://monit-metrics-dev:10012/'


def send(document):
    host = PROD_URL if PRODUCTION else DEV_URL
    print('Sending to: %s' % host)
    return requests.post(host, data=json.dumps(document), headers={"Content-Type": "application/json; charset=UTF-8"})


def send_and_check(document, should_fail=False):
    response = send(document)
    assert((response.status_code in [200]) != should_fail), 'With document: {0}. Status code: {1}. Message: {2}'.format(
        document, response.status_code, response.text)


basic_document = [
    {
        "producer": "invenio",
        "type": "repokpi",
        "type_prefix": "raw",
        "timestamp": 1483696735836,
        "service": "zenodo",
        "env": "prod",
        "records": 433830,
        "visits": 1000,
        "visits_unique": 500,
        "uptime_web": 99.961,
        "uptime_search": 99.961,
        "uptime_files": 99.961,
        "response_time_web": 631.404,
        "response_time_search": 631.404,
        "response_time_files": 631.404,
        "idb_tags": [
            "service",
            "env"
        ],
        "idb_fields": [
            "records",
            "visits",
            "visits_unique",
            "uptime_web",
            "uptime_search",
            "uptime_files",
            "response_time_web",
            "response_time_search",
            "response_time_files"
        ]
    },
    {
        "producer": "invenio",
        "type": "doikpi",
        "type_prefix": "raw",
        "timestamp": 1483696735836,
        "doi_prefix": "10.5281",
        "doi_success": 710383,
        "doi_failed": 17164,
        "idb_tags": [
            "doi_prefix"
        ],
        "idb_fields": [
            "doi_success",
            "doi_failed"
        ]
    }
]

send_and_check(basic_document)
