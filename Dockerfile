# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# KPIit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

FROM python:3.6

RUN apt-get update -y && apt-get upgrade -y
RUN apt-get install -y git curl vim
RUN pip install --upgrade setuptools wheel pip

# Install KPIit
ENV WORKING_DIR=/opt/kpiit

# copy everything inside /src
RUN mkdir -p ${WORKING_DIR}/src
COPY ./ ${WORKING_DIR}/src
WORKDIR ${WORKING_DIR}/src

# Install
RUN ./scripts/bootstrap

# Set folder permissions
RUN chgrp -R 0 ${WORKING_DIR} && \
    chmod -R g=u ${WORKING_DIR}

RUN useradd kpiit --uid 1000 --gid 0 && \
    chown -R kpiit:root ${WORKING_DIR}
USER 1000
