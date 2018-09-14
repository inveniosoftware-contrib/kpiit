# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""KPIit."""

from enum import Enum

from kpiit.config import config
from kpiit.version import __version__


class Service(Enum):
    """Available service types."""

    CDS = config['cds_service']
    CDS_VIDEOS = config['cds_videos_service']
    COD = config['cod_service']
    ZENODO = config['zenodo_service']


class Env(Enum):
    """OpenShift environments."""

    PROD = 'prod'
    QA = 'qa'


__all__ = ('__version__', )
