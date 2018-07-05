# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Metrics module."""

from .doi import DOIMetric
from .records import RecordsMetric
from ..providers import DataCiteProvider, JSONURLProvider


# Record metrics

zenodo_records_metric = RecordsMetric(
    name='zenodo_records',
    provider=JSONURLProvider(
        'https://zenodo.org/api/records/?all_versions'
    )
)

cds_videos_records_metric = RecordsMetric(
    name='cds_videos_records',
    provider=JSONURLProvider(
        'https://videos.cern.ch/api/records/'
    )
)

cod_records_metric = RecordsMetric(
    name='cod_records',
    provider=JSONURLProvider(
        'http://opendata.cern.ch/api/records/'
    )
)

# DOI metrics

doi_attrs = ('doi_total', 'doi_2018', 'doi_2017')

zenodo_doi_metric = DOIMetric(
    name='zenodo_doi',
    provider=DataCiteProvider(
        'CERN - CERN - European Organization for Nuclear Research',
        'CERN.ZENODO',
        doi_attrs
    )
)

cds_videos_doi_metric = DOIMetric(
    name='cds_videos_doi',
    provider=DataCiteProvider(
        'CERN - CERN - European Organization for Nuclear Research',
        'CERN.CDS',
        doi_attrs
    )
)

opendata_doi_metric = DOIMetric(
    name='opendata_doi',
    provider=DataCiteProvider(
        'CERN - CERN - European Organization for Nuclear Research',
        'CERN.OPENDATA',
        doi_attrs
    )
)
