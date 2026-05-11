select
    url,
    page_group,
    owner_team,
    priority_tier,
    observability_status,
    case
        when observability_status = 'critical' then 'money_page_indexability_loss'
        when response_ms >= 600 then 'crawl_latency_spike'
        when impression_change_rate <= -0.15 then 'search_demand_drop'
        else 'none'
    end as anomaly_type,
    case
        when observability_status = 'critical' then 95
        when response_ms >= 600 then 76
        when impression_change_rate <= -0.15 then 71
        else 18
    end as severity_score,
    case
        when observability_status = 'critical' then 'remove noindex and recrawl immediately'
        when response_ms >= 600 then 'investigate template latency and edge path'
        when impression_change_rate <= -0.15 then 'review title coverage, cannibalization, and query drift'
        else 'monitor trend'
    end as operator_action
from {{ ref('mart_url_observability') }}
where observability_status <> 'stable'
order by severity_score desc

