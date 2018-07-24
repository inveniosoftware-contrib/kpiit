# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Service Now provider."""


class ServiceNow(object):
    CERN_TRAINING_INSTANCE = 'https://cerntraining.service-now.com'

    def __init__(self, table_name, instance):
        self.table_name = table_name
        self.instance = instance
        self.source_type = 'table'
        self.version = 2
        self.params = {}

    def where(self, **kwargs):
        self.and_(**kwargs)
        return self

    def and_(self, **kwargs):
        for key, value in kwargs.items():
            self.add_query_param('sysparm_query', key, value)
            self.add_query_param('sysparm_query', '^')
        return self

    def or_(self, **kwargs):
        self.add_query_param('sysparm_query', '^OR')
        return self

    def limit(self, limit_count=None):
        if limit_count is not None:
            self.add_param('sysparm_limit', limit_count)

    def count(self):
        self.source_type = 'stats'
        self.version = 1
        return self

    def orderby(self, *fields, asc=None, desc=None):
        value = '^'.join(fields)
        if asc == False or desc == True:
            value = value + '^DESC'
        self.add_param('sysparm_orderby', value)

    def add_param(self, key, value):
        if key not in self.params:
            self.params[key] = []
        self.params[key].append(value)

    def add_query_param(self, param, key, value=None):
        if param not in self.params:
            self.params[param] = []
        query = self.params[param]

        if value is None:
            query.append(key)
        else:
            if isinstance(value, bool):
                value = str(value).lower()
            else:
                value = str(value)

            query.append('{key}={value}'.format(
                key=key,
                value=value
            ))

    def build_query(self):
        query = ['/api/now/v{version}/{type}/{table}/'.format(
            version=self.version,
            type=self.source_type,
            table=self.table_name
        )]
        return ''.join(query)

    def __str__(self):
        return self.build_query()

    def __repr__(self):
        return 'ServiceNow(instance={inst}, table={tbl}, query={q})'.format(
            inst=self.instance, tbl=self.table_name, q=str(self)
        )

    @classmethod
    def query(cls, table_name, instance=CERN_TRAINING_INSTANCE):
        return cls(table_name, instance)


result = ServiceNow.query('incident').where(
    active=False, test='asdf').and_(hey=1).or_(asdf=1)

print(result)
print(repr(result))
