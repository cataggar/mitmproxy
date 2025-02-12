
import os
import OpenSSL
import socket

import OpenSSL.SSL

def get_monitoring_config():
    context = OpenSSL.SSL.Context(OpenSSL.SSL.TLSv1_2_METHOD)
    # context = OpenSSL.SSL.Context(OpenSSL.SSL.TLS_METHOD)
    client_cert = os.path.expanduser('~/certs/gcs.ppe.monitoring.core.windows.net.pem')
    context.use_privatekey_file(client_cert)
    context.use_certificate_chain_file(client_cert)
    context.set_alpn_protos([b'http/1.1'])

    connection = OpenSSL.SSL.Connection(context, socket.socket(socket.AF_INET, socket.SOCK_STREAM))
    connection.connect(('gcs.ppe.monitoring.core.windows.net', 443))
    connection.set_connect_state()

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
