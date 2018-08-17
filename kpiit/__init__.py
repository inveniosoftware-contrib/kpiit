# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""KPIit."""

from enum import Enum

from kpiit.version import __version__


class Service(Enum):
    """Available service types."""

    CDS = 'cds'
    CDS_VIDEOS = 'cds_videos'
    COD = 'cod'
    ZENODO = 'zenodo'


class Env(Enum):
    """OpenShift environments."""

    PROD = 'prod'
    QA = 'qa'


__all__ = ('__version__', )
