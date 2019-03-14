# Example Usage
import prometheus_connect
url="www.example-prom-url.com"
token='Auth_token'

prom = prometheus_connect.PrometheusConnect(url=url, token=token)

labels = {'pod':'prometheus-k8s-0', '_id': 'f716a8c8-5d4e-417a-a95c-742c2bbcd3d2'}
metric_data = (prom.get_metric_range_data(metric_name='up', start_time='20m', label_config=labels, chunk_size='10m', store_locally=True))

prom.pretty_print_metric(metric_data)
