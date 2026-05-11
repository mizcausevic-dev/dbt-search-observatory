select
    url,
    page_group,
    template,
    owner_team,
    cast(expected_refresh_days as integer) as expected_refresh_days,
    priority_tier,
    cast(is_money_page as boolean) as is_money_page
from {{ ref('url_inventory') }}

