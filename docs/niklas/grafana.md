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
* line diagram och how the used space and maximum space has changed over time

Do we want any stats related to 'max_files' and 'used_files'?

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
tickets were created etc

# Support waiting in line

* Show line graph of how support waiting in line has changed over time
* ???

Dashboard

*
* Should be able to switch between these sources:
    - CDS Videos
    - Zenodo
    - COD
    - Total (all sources combined)
    Note: Use variables in Grafana for this?

SELECT last("percent_used_bytes")
FROM "raw"."quota_usage"
WHERE ("path" =~ /.*media.*zenodo/ AND ('$src' = '(CDS Videos|Zenodo|COD)' OR '$src' = '(Zenodo)' OR '$src' = '(CDS Videos|Zenodo)' OR '$src' = '(Zenodo|COD)')) AND $timeFilter GROUP BY time($__interval) fill(null)

SELECT last("percent_used_bytes")
FROM "raw"."quota_usage"
WHERE
    (("path" =~ /.*media.*zenodo/ OR "path" =~ /.*media.*cds/) AND 
    '$src' = '(CDS Videos|Zenodo|COD)')
    AND $timeFilter
GROUP BY time($__interval) fill(null)

SELECT last("percent_used_bytes")
FROM "raw"."quota_usage"
WHERE
    ("path" =~ /.*media.*zenodo/ AND 
        ('$src' = '(Zenodo)' OR 
         '$src' = '(CDS Videos|Zenodo)' OR 
         '$src' = '(Zenodo|COD)'))
    AND $timeFilter
GROUP BY time($__interval) fill(null)



SELECT last("percent_used_bytes")
FROM "raw"."quota_usage"
WHERE (
    ('$src' =~ /^CDS Videos$/ AND "path" =~ /.*media.*cds/) OR
    ('$src' =~ /^Zenodo$/ AND "path" =~ /.*media.*zenodo/) OR
    ('$src' =~ /^COD$/ AND "path" =~ /.*eos.*opendata.*/) OR
    ('$src' = 'All' AND ("path" =~ /.*media.*(cds|zenodo)/ OR "path" =~ /.*eos.*opendata.*/))
)
AND $timeFilter GROUP BY time($__interval) path