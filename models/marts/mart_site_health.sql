select
    count(*) as tracked_urls,
    sum(case when is_money_page then 1 else 0 end) as money_pages,
    sum(case when observability_status = 'critical' then 1 else 0 end) as critical_urls,
    sum(case when observability_status = 'watch' then 1 else 0 end) as watch_urls,
    round(avg(response_ms), 1) as avg_response_ms,
    round(sum(five_day_clicks)::double / nullif(sum(five_day_impressions)::double, 0), 4) as blended_ctr,
    max(latest_crawl_at) as latest_crawl_at
from {{ ref('mart_url_observability') }}

