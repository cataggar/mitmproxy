import os
import socket
from OpenSSL import SSL
from mitmproxy.net import tls

def get_monitoring_config():
    client_cert = os.path.expanduser('~/certs/gcs.ppe.monitoring.core.windows.net.pem')

    context = tls.create_proxy_server_context(
        method=tls.Method.TLS_CLIENT_METHOD,
        min_version=tls.DEFAULT_MIN_VERSION,
        max_version=tls.DEFAULT_MAX_VERSION,
        cipher_list=None,
        ecdh_curve=None,
        verify=tls.Verify.VERIFY_NONE,
        ca_path=None,
        ca_pemfile=None,
        client_cert=client_cert,
        legacy_server_connect=True)
    
    connection = SSL.Connection(context, socket.socket(socket.AF_INET, socket.SOCK_STREAM))
    connection.connect(('gcs.ppe.monitoring.core.windows.net', 443))
    request = (
        b'GET /api/agent/v2/Test/SkyLink/MonitoringConfiguration/?Namespace=SkyLink&Version=Ver2v0.109&OSType=Linux HTTP/1.1\r\n'
        b'Host: gcs.ppe.monitoring.core.windows.net\r\n\n'
    )
    connection.send(request)

    res_buf_size = 1024
    response = b''
    while True:
        data = connection.recv(res_buf_size)
        response += data
        if len(data) < res_buf_size:
            break
    connection.shutdown()
    connection.close()
    return response

response = get_monitoring_config()
print(response)
