select
    url,
    anomaly_type,
    severity_score,
    operator_action
from observatory.mart_anomaly_flags
order by severity_score desc;

