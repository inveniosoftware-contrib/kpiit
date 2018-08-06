# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Service Now provider."""

import os

import requests
import requests.exceptions
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
    Service.CDS: 'CERN Document Server',
    Service.CDS_VIDEOS: 'MultiMedia Archive',
    Service.COD: 'Open Data Repository',
    Service.ZENODO: 'Zenodo Repository'
}


class ServiceNowQuery(object):
    """Service Now query builder."""

    def __init__(self, table_name, instance=INSTANCE_URLS['test']):
        """Initiate the Service Now query."""
        self.table_name = table_name
        self.instance = instance
        self.reset()

    @property
    def url(self):
        """Getter for the full query URL."""
        return '{instance}{path}'.format(
            instance=self.instance,
            path=str(self)
        )

    def reset(self):
        """Reset the query to the starting values."""
        self.source_type = 'table'
        self.api_version = 2
        self.params = {}

    def where(self, *args, **kwargs):
        """
        Start a new query filter adding each keyword argument as a filter.

        Each keyword argument will be connected with an AND.
        """
        self.params['sysparm_query'] = self._append_params([], *args, **kwargs)
        return self

    def and_(self, *args, **kwargs):
        """Add additional filters connected with an AND."""
        query = self.params['sysparm_query']
        self._append_params(query, *args, **kwargs)
        return self

    def or_(self, *args, **kwargs):
        """Add additional filters connected with an OR."""
        query = self.params['sysparm_query']
        self._append_params(query, use_or=True, *args, **kwargs)
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

    def avg(self, *fields):
        """Aggregate fields by taking the average of the values."""
        self.aggregate('avg', *fields)
        return self

    def sum(self, *fields):
        """Aggregate fields by taking the sum of the values."""
        self.aggregate('sum', *fields)
        return self

    def min(self, *fields):
        """Aggregate fields by taking the minimum of the values."""
        self.aggregate('min', *fields)
        return self

    def max(self, *fields):
        """Aggregate fields by taking the maximum of the values."""
        self.aggregate('max', *fields)
        return self

    def aggregate(self, op, field, *fields):
        """Add aggregate operation for the given fields."""
        fields = [field, *fields]
        self.source_type = 'stats'
        self.api_version = 1
        self.params['sysparm_{}_fields'.format(op)] = ','.join(fields)
        return self

    def _append_params(self, query, *args, use_or=False, **kwargs):
        """Append more parameters to the query."""
        for arg in args:
            if query:
                query.append('^OR' if use_or else '^')
            query.append(arg)
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

    def _collect_record_count(self, table):
        """Extract record count from JSON object."""
        functional_element = FUNC_ELEMENT_IDS[self.functional_element]

        query = ServiceNowQuery(table, self.instance).where(
            'assignment_groupSTARTSWITH{}'.format(functional_element),
            'stateNOT IN4,3,7,6,8'  # only select tickets that are not closed
        ).max('u_reassignment_counter_fe').count()

        res_json = self.auth_get(query.url)

        return res_json['result']['stats']

    def _collect_stc(self, table):
        """Collect waiting time from Service Now."""
        functional_element = FUNC_ELEMENT_IDS[self.functional_element]

        query = ServiceNowQuery(table, self.instance).where(
            'assignment_groupSTARTSWITH{}'.format(functional_element),
        ).avg('calendar_stc')

        res_json = self.auth_get(query.url)

        return res_json['result']['stats']['avg']['calendar_stc']

    def collect(self):
        """Collect support stats from Service Now."""
        req_res = self._collect_record_count(REQ_TABLE)
        inc_res = self._collect_record_count(INC_TABLE)

        try:
            req_fe_count = int(req_res['max']['u_reassignment_counter_fe'])
        except ValueError:
            req_fe_count = 0

        try:
            inc_fe_count = int(inc_res['max']['u_reassignment_counter_fe'])
        except ValueError:
            inc_fe_count = 0

        return {
            'support_requests': req_res['count'],
            'support_incidents': inc_res['count'],
            'reassignment_count': req_fe_count + inc_fe_count,
            'incident_stc': self._collect_stc(INC_TABLE)
        }

    @classmethod
    def auth_get(cls, url, user=SNOW_USER, password=SNOW_PASS):
        """Perform an authenticated GET request."""
        response = requests.get(url, auth=(user, password))
        if response.status_code != 200:
            raise requests.exceptions.HTTPError(response=response)
        return response.json()
