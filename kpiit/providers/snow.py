# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Service Now provider."""


class ServiceNowQuery(object):
    """Service Now query builder."""

    CERN_TRAINING_INSTANCE = 'https://cerntraining.service-now.com'

    def __init__(self, table_name, instance=CERN_TRAINING_INSTANCE):
        """Initiate the Service Now query."""
        self.table_name = table_name
        self.instance = instance
        self.source_type = 'table'
        self.api_version = 2
        self.params = {}

    @property
    def url(self):
        """Getter for the full query URL."""
        return '{instance}{path}'.format(
            instance=self.instance,
            path=str(self)
        )

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
