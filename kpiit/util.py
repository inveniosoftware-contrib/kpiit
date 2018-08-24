# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Utility functions."""

from importlib import import_module


def load_target(abs_path):
    """Load and return class/function object from an absolute path."""
    path_split = abs_path.split('.')

    module_path = '.'.join(path_split[:-1])
    obj_name = path_split[-1]

    module_obj = import_module(module_path)
    target_obj = getattr(module_obj, obj_name)

    return target_obj


def args(*args, **kwargs):
    """Get function arguments as a dictionary."""
    return dict(args=args, kwargs=kwargs)
