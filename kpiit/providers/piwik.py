# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Piwik provider."""

import subprocess

import cern_sso
import requests
import requests.exceptions
from celery.utils.log import get_task_logger

from kpiit.config import config
from kpiit.providers.base import BaseProvider

BASE_URL = config['providers']['piwik']['base_url']
URL = config['providers']['piwik']['url']

logger = get_task_logger(__name__)


class Piwik(object):
    """Static base class for accessing the Piwik API."""

    name = None
    cookie = None

    @classmethod
    def krb_ticket(cls, principal, keytab_file):
        """Retrieve the Kerberos ticket for `principal`."""
        try:
            ret = subprocess.run(['kinit', principal, '-k', '-t', keytab_file])
            ret.check_returncode()
        except subprocess.CalledProcessError:
            logger.error('Failed to retrieve Kerberos ticket')

    @classmethod
    def krb_cookie(cls):
        """Retrieve the Kerberos cookie.

        Note: Make sure the user has a valid Kerberos ticket before retrieving
        the cookie.
        """
        return cern_sso.krb_sign_on(BASE_URL)

    @classmethod
    def get(cls, url):
        """Make a GET API call to Piwik.

        TODO: Handle unauthorized API calls.

        :param str url: API url
        """
        if cls.cookie is None:
            cls.krb_ticket(
                config['providers']['piwik']['principal'],
                config['providers']['piwik']['keytab_file']
            )
            cls.cookie = cls.krb_cookie()
        response = requests.get(url, cookies=cls.cookie)
        return response.json()

    @classmethod
    def build_url(cls, module, method, file_format='json', filter_limit=-1,
                  **kwargs):
        """Build API URL from the given parameters.

        :param str module: API module (e.g. VisitsSummary)
        :param str method: API method (e.g. getVisits)
        :param str file_format: response file_format, defaults to 'json'
        :param int filter_limit: max number of records to get, defaults to -1
        :return: generated URL
        """
        kwargs['method'] = '{}.{}'.format(module, method)
        kwargs['format'] = file_format
        if filter_limit != -1:
            kwargs['filter_limit'] = filter_limit
        query = ['{}={}'.format(key, value)
                 for key, value in kwargs.items()
                 if value is not None and value]
        return URL.format(query='&'.join(query))
        # return BASE_URL + 'index.php?module=API&' + '&'.join(query)


class PiwikAPI(Piwik):
    """Piwik API module."""

    NAME = 'API'

    @classmethod
    def piwik_version(cls):
        """Get the Piwik API version."""
        data = cls.get(cls.build_url(cls.name, cls.piwik_version.__name__))
        return data['value']


class PiwikVisitsSummary(Piwik):
    """Piwik API VisitsSummary module."""

    NAME = 'VisitsSummary'

    @classmethod
    def visits(cls, site_id, period, date, segment=''):
        """Get number of visits for a site.

        :param int site_id: ID of website
        :param str period: range of when visits are counted
        :param str date: date for when visits are counted
        :param segment: TODO, defaults to ''
        :return: number of visits
        :rtype: str
        """
        url = cls.build_url(cls.name, cls.getVisits.__name__, site_id=site_id,
                            period=period, date=date, segment=segment)
        data = cls.get(url)
        return data['value']

    @classmethod
    def unique_visitors(cls, site_id, period, date, segment=''):
        """Get number of unique visitors for a site.

        :param int site_id: ID of website
        :param str period: range of when visits are counted
        :param str date: date for when visits are counted
        :param segment: TODO, defaults to ''
        :return: number of unique visitors
        :rtype: str
        """
        url = cls.build_url(cls.name, cls.unique_visitors.__name__,
                            site_id=site_id, period=period, date=date,
                            segment=segment)
        data = cls.get(url)
        return data['value']


class PiwikProvider(BaseProvider):
    """Piwik provider."""

    def __init__(self, site_id, period='day', date='yesterday'):
        """Initiate the Piwik provider."""
        self.site_id = site_id
        self.period = period
        self.date = date

    def collect(self):
        """Collect support stats from Service Now."""
        visits = PiwikVisitsSummary.visits(
            self.site_id, self.period, self.date)
        unique_visits = PiwikVisitsSummary.unique_visitors(
            self.site_id, self.period, self.date)

        return {
            'visits': visits,
            'visits_unique': unique_visits
        }
