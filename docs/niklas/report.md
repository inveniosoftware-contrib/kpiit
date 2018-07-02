# KPIs dashboard for Invenio-Related Services

(~15-20 pages (incl. all pages)?)

## Title Page

## Project Specification
## Abstract

## TOC

## Acknowledgments
## Introduction

## KPIs

General info about what KPIs are, which information was collected and how CERN
is using KPIs to find what works/doesn't work.

### Harvester

Intro to the harvester.

#### Tasks

Info about Celery and what the harvester is doing.

#### System Architecture

Info about Metric, Provider, Publisher, etc.

#### Deployment (low priority)

Information about how the harvester was deployed (openshift/docker, etc)

## Grafana

Intro to Grafana (like dashboards, panels, data sources, etc)

### Dashboard

How was the dashboard designed and what does it include?

### InfluxDB

Info about time series data and what InfluxDB is.

## Invenio (will expand this once the 2nd part starts)

## Results & Conclusions
## References





# Grafana Dashboard Layouts

Discussion on how to design the layout for the KPI dashboard.

# # Data

Would look good regardless but a good layout may make it easier to understand.

# of records

Number of records would work with:

* Line plots: to see the trends in increase/decrease # of records
* Include mean average of number of records
* Time interval to get the latest data values from the database
* Use time interval to get the hours with the most submitted records

# of visits/unique

* Number of visits can be shown as a line diagram
* Use a bar chart to display during which hours the visitors attended

# Files (TBs)

* Storage uses (percentage)
* line diagram och how the used space has changed over time

# Uptime

Display the following:
* Which services are currently up and running?
* How much downtime the past X hours/days/weeks/months (in percentage)

# Response time

* How quickly is the sever responding to requests?
* Does the response time depend anything on the time of the day

# # of support tickets

* See how # of tickets have increased over time
* Could be displayed as a line graph with exra details about when the support
tickets were created to get a better spread internally.

# Support waiting in line

* Show line graph of how support waiting in line has changed over time
* 