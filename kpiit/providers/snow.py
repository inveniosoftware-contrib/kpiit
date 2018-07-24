# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Service Now provider."""


class ServiceNowQuery(object):
    CERN_TRAINING_INSTANCE = 'https://cerntraining.service-now.com'

    def __init__(self, table_name, instance=CERN_TRAINING_INSTANCE):
        self.table_name = table_name
        self.instance = instance
        self.source_type = 'table'
        self.api_version = 2
        self.params = {}

    @property
    def url(self):
        return '{instance}{path}'.format(
            instance=self.instance,
            path=str(self)
        )

    def where(self, **kwargs):
        self.params['sysparm_query'] = self._build_query([], **kwargs)
        return self

    def and_(self, **kwargs):
        query = self.params['sysparm_query']
        self._build_query(query, **kwargs)
        return self

    def or_(self, **kwargs):
        query = self.params['sysparm_query']
        self._build_query(query, use_or=True, **kwargs)
        return self

    def limit(self, limit_count):
        self.params['sysparm_limit'] = str(limit_count)
        return self

    def count(self):
        self.source_type = 'stats'
        self.api_version = 1
        self.params['sysparm_count'] = 'true'
        return self

    def orderby(self, *fields, desc=False):
        value = '^'.join(fields)
        if desc:
            value = value + '^DESC'
        self.params['sysparm_orderby'] = value
        return self

    def _build_query(self, query, use_or=False, **kwargs):
        for key, value in kwargs.items():
            if query:
                query.append('^OR' if use_or else '^')
            query.append(self._clean_param(key, value))
        return query

    def _clean_param(self, key, value):
        if isinstance(value, bool):
            value = str(value).lower()
        else:
            value = str(value)

        return '{key}={value}'.format(
            key=key,
            value=value
        )

    def __str__(self):
        query = ['/api/now/v{version}/{type}/{table}'.format(
            version=self.api_version,
            type=self.source_type,
            table=self.table_name
        )]
        params = []
        for index, (key, value_list) in enumerate(self.params.items()):
            if index == 0:
                query.append('?')
            params.append(self._get_param_str(key, value_list))
        return ''.join(query) + '&'.join(params)

    def __repr__(self):
        return 'ServiceNow(instance="{}", table={}, query="{}")'.format(
            self.instance,
            self.table_name,
            str(self)
        )

    @classmethod
    def _get_param_str(self, key, values):
        return '{}={}'.format(key, ''.join(values))
