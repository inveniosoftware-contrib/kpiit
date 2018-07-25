# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Service Now provider."""

import os

import requests
from celery.utils.log import get_task_logger

from kpiit import Service

from ..models import Provider

logger = get_task_logger(__name__)

SNOW_USER = os.getenv('SNOW_USER')
SNOW_PASS = os.getenv('SNOW_PASS')

INC_TABLE = 'incident'
REQ_TABLE = 'u_request_fulfillment'

INSTANCE_URLS = dict(
    prod=None,
    test='https://cerntraining.service-now.com'
)

# Functional element IDs
FUNC_ELEMENT_IDS = {
    Service.CDS: 'ea56e9860a0a8c0a0186aeaa533e811a',
    Service.CDS_VIDEOS: 'e993ff170a0a8c0a01e036015c55c628',
    Service.ZENODO: 'e93478690a0a8c0a009abf9422a74c71'
}


class ServiceNowQuery(object):
    """Service Now query builder."""

    def __init__(self, table_name, instance=INSTANCE_URLS['test']):
        """Initiate the Service Now query."""
        self.table_name = table_name
        self.instance = instance
        self.init()

    @property
    def url(self):
        """Getter for the full query URL."""
        return '{instance}{path}'.format(
            instance=self.instance,
            path=str(self)
        )

    def init(self):
        """Reset the query to the starting values."""
        self.source_type = 'table'
        self.api_version = 2
        self.params = {}

    def where(self, **kwargs):
        """
        Start a new query filter adding each keyword argument as a filter.

        Each keyword argument will be connected with an AND.
        """
        self.params['sysparm_query'] = self._append_params([], **kwargs)
        return self

    def and_(self, **kwargs):
        """Add additional filters connected with an AND."""
        query = self.params['sysparm_query']
        self._append_params(query, **kwargs)
        return self

    def or_(self, **kwargs):
        """Add additional filters connected with an OR."""
        query = self.params['sysparm_query']
        self._append_params(query, use_or=True, **kwargs)
        return self

    def limit(self, limit_count):
        """Limit the number of items in the result."""
        self.params['sysparm_limit'] = str(limit_count)
        return self

    def count(self):
        """Return the count of the number of items."""
        self.source_type = 'stats'
        self.api_version = 1
        self.params['sysparm_count'] = 'true'
        return self

    def orderby(self, *fields, desc=False):
        """Order the results by field(s) where ASC is the default."""
        value = '^'.join(fields)
        if desc:
            value = value + '^DESC'
        self.params['sysparm_orderby'] = value
        return self

    def _append_params(self, query, use_or=False, **kwargs):
        """Append more parameters to the query."""
        for key, value in kwargs.items():
            if query:
                query.append('^OR' if use_or else '^')
            query.append(self._clean_param(key, value))
        return query

    def _clean_param(self, key, value):
        """Return a clean key=value string."""
        if isinstance(value, bool):
            value = str(value).lower()
        else:
            value = str(value)

        return '{}={}'.format(key, value)

    def __str__(self):
        """Return the query formatted as a string excluding the URL."""
        query = ['/api/now/v{version}/{type}/{table}'.format(
            version=self.api_version,
            type=self.source_type,
            table=self.table_name
        )]
        params = []
        for index, (key, values) in enumerate(self.params.items()):
            if index == 0:
                query.append('?')
            params.append('{}={}'.format(key, ''.join(values)))
        return ''.join(query) + '&'.join(params)

    def __repr__(self):
        """Representation of the query object."""
        return 'ServiceNow(instance="{}", table={}, query="{}")'.format(
            self.instance,
            self.table_name,
            str(self)
        )


class ServiceNowProvider(Provider):
    """Service Now provider."""

    def __init__(self, functional_element, instance=INSTANCE_URLS['test']):
        """Initiate the Service Now provider."""
        self.functional_element = functional_element
        self.instance = instance

    def _collect_support_requests(self):
        """Collect support request count from Serivce Now."""
        return self._get_record_count(REQ_TABLE)

    def _collect_support_incidents(self):
        """Collect support incident count from Serivce Now."""
        return self._get_record_count(INC_TABLE)

    def _get_record_count(self, table):
        """Extract record count from JSON object."""
        func_element_id = FUNC_ELEMENT_IDS[self.functional_element]

        query = ServiceNowQuery(table, self.instance).where(
            u_functional_element=func_element_id,
            active=True
        ).count()

        # TODO: Perform error checking on return response
        res = self.auth_get(query.url)
        res_json = res.json()

        return res_json['result']['stats']['count']

    def collect(self):
        """Collect support stats from Service Now."""
        support_requests = self._collect_support_requests()
        support_incidents = self._collect_support_incidents()

        return {
            'support_requests': support_requests,
            'support_incidents': support_incidents
        }

    @classmethod
    def auth_get(cls, url, user=SNOW_USER, password=SNOW_PASS):
        """Perform an authenticated GET request."""
        return requests.get(url, auth=(user, password))
