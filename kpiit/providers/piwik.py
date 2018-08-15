# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Piwik provider."""

import os
import subprocess

import cern_sso
import requests
import requests.exceptions
from celery.utils.log import get_task_logger

from kpiit import Service

from ..models import Provider

logger = get_task_logger(__name__)


class Piwik(object):
    """Static base class for accessing the Piwik API."""

    BASE_URL = 'https://piwikui.web.cern.ch/piwikui/'
    NAME = None
    COOKIE = None

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
        return cern_sso.krb_sign_on(cls.BASE_URL)

    @classmethod
    def get(cls, url):
        """Make a GET API call to Piwik.

        TODO: Handle unauthorized API calls.

        :param str url: API url
        """
        if cls.COOKIE is None:
            cls.krb_ticket('n.persson@CERN.CH', 'n.persson.keytab')
            cls.COOKIE = cls.krb_cookie()
        response = requests.get(url, cookies=cls.COOKIE)
        return response.json()

    @classmethod
    def build_url(cls, module, method, format='json', filter_limit=-1,
                  **kwargs):
        """Build API URL from the given parameters.

        :param str module: API module (e.g. VisitsSummary)
        :param str method: API method (e.g. getVisits)
        :param str format: response format, defaults to 'json'
        :param int filter_limit: max number of records to get, defaults to -1
        :return: generated URL
        """
        kwargs['method'] = '{}.{}'.format(module, method)
        kwargs['format'] = format
        if filter_limit != -1:
            kwargs['filter_limit'] = filter_limit
        query = ['{}={}'.format(key, value)
                 for key, value in kwargs.items()
                 if value is not None and value]
        return cls.BASE_URL + 'index.php?module=API&' + '&'.join(query)


class PiwikAPI(Piwik):
    """Piwik API module."""

    NAME = 'API'

    @classmethod
    def getPiwikVersion(cls):
        """Get the Piwik API version."""
        data = cls.get(cls.build_url(cls.NAME, cls.getPiwikVersion.__name__))
        return data['value']


class PiwikVisitsSummary(Piwik):
    """Piwik API VisitsSummary module."""

    NAME = 'VisitsSummary'

    @classmethod
    def getVisits(cls, idSite, period, date, segment=''):
        """Get number of visits for a site.

        :param int idSite: ID of website
        :param str period: range of when visits are counted
        :param str date: date for when visits are counted
        :param segment: TODO, defaults to ''
        :return: number of visits
        :rtype: str
        """
        url = cls.build_url(cls.NAME, cls.getVisits.__name__, idSite=idSite,
                            period=period, date=date, segment=segment)
        data = cls.get(url)
        return data['value']

    @classmethod
    def getUniqueVisitors(cls, idSite, period, date, segment=''):
        """Get number of unique visitors for a site.

        :param int idSite: ID of website
        :param str period: range of when visits are counted
        :param str date: date for when visits are counted
        :param segment: TODO, defaults to ''
        :return: number of unique visitors
        :rtype: str
        """
        url = cls.build_url(cls.NAME, cls.getUniqueVisitors.__name__,
                            idSite=idSite, period=period, date=date,
                            segment=segment)
        data = cls.get(url)
        return data['value']


class PiwikProvider(Provider):
    """Piwik provider."""

    def __init__(self, site_id, period='day', date='yesterday'):
        """Initiate the Piwik provider."""
        self.site_id = site_id
        self.period = period
        self.date = date

    def collect(self):
        """Collect support stats from Service Now."""
        visits = PiwikVisitsSummary.getVisits(
            self.site_id, self.period, self.date)
        unique_visits = PiwikVisitsSummary.getUniqueVisitors(
            self.site_id, self.period, self.date)

        return {
            'visits': visits,
            'visits_unique': unique_visits
        }
