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