
import os
import OpenSSL
from OpenSSL import crypto
from OpenSSL import SSL
import socket

import OpenSSL.SSL
# from mitmproxy.net.tls import make_master_secret_logger
# from mitmproxy import tls
from mitmproxy.net import tls #as net_tls
from mitmproxy.addons import tlsconfig
from mitmproxy.test import taddons

def get_monitoring_config():
    # context = OpenSSL.SSL.Context(OpenSSL.SSL.TLSv1_2_METHOD)
    # context = OpenSSL.SSL.Context(OpenSSL.SSL.TLS_METHOD)
    client_cert = os.path.expanduser('~/certs/gcs.ppe.monitoring.core.windows.net.pem')

    context = tls.create_proxy_server_context(
        method=tls.Method.TLSv1_2_METHOD,
        # min_version=tls.DEFAULT_MIN_VERSION,
        min_version=tls.DEFAULT_MAX_VERSION,
        max_version=tls.DEFAULT_MAX_VERSION,
        cipher_list=None,
        ecdh_curve=None,
        verify=tls.Verify.VERIFY_NONE,
        ca_path=None,
        ca_pemfile=None,
        client_cert=client_cert,
        legacy_server_connect=False)
    
    context.use_privatekey_file(client_cert)
    context.use_certificate_chain_file(client_cert)
    context.set_alpn_protos([b'http/1.1'])

    connection = OpenSSL.SSL.Connection(context, socket.socket(socket.AF_INET, socket.SOCK_STREAM))
    connection.connect(('gcs.ppe.monitoring.core.windows.net', 443))

    # config = tlsconfig.TlsConfig()


    # def test_tls_start_server_verify_failed(self):
    # ta = tlsconfig.TlsConfig()
    # with taddons.context(ta) as tctx:
    #     ctx = _ctx(tctx.options)
    #     ctx.client.alpn_offers = [b'http/1.1']
    #     ctx.client.cipher_list = ["TLS_AES_256_GCM_SHA384", "ECDHE-RSA-AES128-SHA"]
    #     ctx.server.address = ("gcs.ppe.monitoring.core.windows.net", 443)

    #     tls_start = tls.TlsData(ctx.server, context=ctx)
    #     ta.tls_start_server(tls_start)
    #     tssl_client = tls_start.ssl_conn
        # tssl_server = test_tls.SSLTest(server_side=True)
        # self.do_handshake(tssl_client, tssl_server)

    # cctx = tls.create_proxy_server_context(
    #     method=tls.Method.TLS_CLIENT_METHOD,
    #     min_version=tls.DEFAULT_MIN_VERSION,
    #     max_version=tls.DEFAULT_MAX_VERSION,
    #     cipher_list=None,
    #     ecdh_curve=None,
    #     verify=tls.Verify.VERIFY_NONE,
    #     ca_path=None,
    #     ca_pemfile=None,
    #     client_cert=None,
    #     legacy_server_connect=False,
    # )

    # server.use_certificate(entry.cert.to_pyopenssl())
    # server.use_privatekey(crypto.PKey.from_cryptography_key(entry.privatekey))
    # context.use_privatekey_file(client_cert)
    # context.use_certificate_chain_file(client_cert)

    # client = SSL.Connection(cctx)
    # client.set_connect_state()

    # sctx = tls.create_client_proxy_context(
    #     method=tls.Method.TLS_SERVER_METHOD,
    #     min_version=tls.DEFAULT_MIN_VERSION,
    #     max_version=tls.DEFAULT_MAX_VERSION,
    #     cipher_list=None,
    #     ecdh_curve=None,
    #     chain_file=None,
    #     alpn_select_callback=None,
    #     request_client_cert=False,
    #     extra_chain_certs=(),
    #     dhparams=None,
    # )

# from mitmproxy.net import tls as net_tls

    # cctx = tls.create_proxy_server_context(
    #     method=tls.Method.TLS_CLIENT_METHOD,
    #     min_version=tls.DEFAULT_MIN_VERSION,
    #     max_version=tls.DEFAULT_MAX_VERSION,
    #     cipher_list=None,
    #     ecdh_curve=None,
    #     verify=tls.Verify.VERIFY_NONE,
    #     ca_path=None,
    #     ca_pemfile=None,
    #     client_cert=client_cert,
    #     legacy_server_connect=False,
    # )

    # client = SSL.Connection(cctx)

    # tlsconfig
    # def tls_start_server(self, tls_start: tls.TlsData) -> None:
    #     """Establish TLS or DTLS between proxy and server."""


    # connection = OpenSSL.SSL.Connection(context, socket.socket(socket.AF_INET, socket.SOCK_STREAM))
    # connection = OpenSSL.SSL.Connection(context)
    # connection.connect(('gcs.ppe.monitoring.core.windows.net', 443))
    # connection.set_connect_state()

    # client.set_connect_state()

    # server = SSL.Connection(sctx)
    # server.set_accept_state()

    # server.use_certificate(entry.cert.to_pyopenssl())
    # server.use_privatekey(crypto.PKey.from_cryptography_key(entry.privatekey))
    # client.use_privatekey_file(client_cert)
    # client.use_certificate_chain_file(client_cert)


    # read, write = client, server
    # while True:
    #     try:
    #         read.do_handshake()
    #     except SSL.WantReadError:
    #         write.bio_write(read.bio_read(2**16))
    #     else:
    #         break
    #     read, write = write, read





    # keylog = os.path.expanduser('~/certs/key.log')
    # secret_logger = make_master_secret_logger(keylog)
    # cctx.set_keylog_callback(secret_logger)

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
