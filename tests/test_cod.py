# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""COD tests."""


def test_cod_records(cod_records):
    cod_records.collect()

    assert cod_records.records == 4613
