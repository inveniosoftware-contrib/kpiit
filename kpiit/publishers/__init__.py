# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Publisher instances."""

from enum import Enum

from celery.utils.log import get_task_logger

from kpiit.publishers.cern import CERNMonitPublisher

logger = get_task_logger(__name__)


def doi(prefix, skip_fields=False, save_json=True):
    """Create a DOI publisher instance."""
    return CERNMonitPublisher(
        'doikpi',
        doi_prefix=prefix,
        skip_fields=skip_fields
    )


def repo(service, env, skip_fields=False, save_json=True):
    """Create a repo publisher instance."""
    if isinstance(service, Enum):
        service = service.value

    if isinstance(env, Enum):
        env = env.value

    return CERNMonitPublisher(
        'repokpi',
        service=service,
        env=env,
        skip_fields=skip_fields
    )
