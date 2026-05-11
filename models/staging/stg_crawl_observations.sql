select
    cast(observed_at as timestamp) as observed_at,
    url,
    cast(status_code as integer) as status_code,
    indexability,
    canonical_state,
    cast(response_ms as integer) as response_ms,
    template,
    agent_group
from {{ ref('crawl_observations') }}

