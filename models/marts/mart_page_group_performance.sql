select
    page_group,
    max(owner_team) as owner_team,
    sum(five_day_impressions) as impressions_5d,
    sum(five_day_clicks) as clicks_5d,
    round(avg(avg_ctr), 4) as avg_ctr,
    round(avg(avg_position), 2) as avg_position,
    max(case when observability_status = 'critical' then 1 else 0 end) as has_critical_url,
    round(avg(response_ms), 1) as avg_response_ms
from {{ ref('mart_url_observability') }}
group by 1
order by impressions_5d desc

