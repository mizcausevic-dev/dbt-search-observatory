select
    cast(event_date as date) as event_date,
    url,
    query,
    page_group,
    device,
    country,
    cast(impressions as integer) as impressions,
    cast(clicks as integer) as clicks,
    cast(avg_position as double) as avg_position,
    round(cast(clicks as double) / nullif(cast(impressions as double), 0), 4) as ctr
from {{ ref('search_console_daily') }}

