with latest_crawl as (
    select
        url,
        max(observed_at) as latest_observed_at
    from {{ ref('stg_crawl_observations') }}
    group by 1
),
crawl_snapshot as (
    select c.*
    from {{ ref('stg_crawl_observations') }} c
    inner join latest_crawl lc
        on c.url = lc.url
       and c.observed_at = lc.latest_observed_at
),
search_rollup as (
    select
        url,
        max(event_date) as latest_search_date,
        sum(impressions) as five_day_impressions,
        sum(clicks) as five_day_clicks,
        round(avg(avg_position), 2) as avg_position,
        round(avg(ctr), 4) as avg_ctr,
        round(
            (
                max(case when event_date = (select max(event_date) from {{ ref('stg_search_console_daily') }}) then impressions end)
                - min(case when event_date = (select min(event_date) from {{ ref('stg_search_console_daily') }}) then impressions end)
            ) / nullif(min(case when event_date = (select min(event_date) from {{ ref('stg_search_console_daily') }}) then impressions end), 0),
            4
        ) as impression_change_rate
    from {{ ref('stg_search_console_daily') }}
    group by 1
)
select
    inv.url,
    inv.page_group,
    inv.template,
    inv.owner_team,
    inv.expected_refresh_days,
    inv.priority_tier,
    inv.is_money_page,
    sr.latest_search_date,
    sr.five_day_impressions,
    sr.five_day_clicks,
    sr.avg_position,
    sr.avg_ctr,
    sr.impression_change_rate,
    cs.observed_at as latest_crawl_at,
    cs.status_code,
    cs.indexability,
    cs.canonical_state,
    cs.response_ms,
    case
        when cs.indexability = 'noindex' and inv.is_money_page then 'critical'
        when cs.response_ms >= 600 then 'watch'
        when sr.impression_change_rate <= -0.15 then 'watch'
        else 'stable'
    end as observability_status
from {{ ref('stg_url_inventory') }} inv
left join search_rollup sr on inv.url = sr.url
left join crawl_snapshot cs on inv.url = cs.url

