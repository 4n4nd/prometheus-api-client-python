from prometheus_api_client import PrometheusConnect
from prometheus_api_client.utils import parse_datetime
from datetime import timedelta

from requests_auth_aws_sigv4 import AWSSigV4 # pip install requests-auth-aws-sigv4
# Optionally install boto3 if you'd like to use AWS CLI/SDK credentials

region = 'us-east-1'
workspace_id = 'ws-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'

auth = AWSSigV4('aps', region=region)

prom = PrometheusConnect(url=f"https://aps-workspaces.{region}.amazonaws.com/workspaces/{workspace_id}", disable_ssl=False, auth=auth)

# Print all metrics
metrics = prom.all_metrics()
print(metrics)

# Get 'prometheus_ready' metric for the last 15 minutes
start_time = parse_datetime("15m")
end_time = parse_datetime("now")
chunk_size = timedelta(minutes=15)

metric_data = prom.get_metric_range_data(
    metric_name='prometheus_ready',
    start_time=start_time,
    end_time=end_time,
    chunk_size=chunk_size,
)

print(metric_data[0]['values'])
