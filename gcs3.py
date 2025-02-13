import os
import requests
import json

def get_monitoring_config():
    client_cert = os.path.expanduser('~/certs/gcs.ppe.monitoring.core.windows.net.pem')
    url = 'https://gcs.ppe.monitoring.core.windows.net/api/agent/v2/Test/SkyLink/MonitoringConfiguration/?Namespace=SkyLink&Version=Ver2v0.109&OSType=Linux'
    response = requests.get(url, cert=(client_cert, client_cert))
    return response

response = get_monitoring_config()
print(f'status code: {response.status_code}')
j = response.json()
print(json.dumps(j, indent=2))
