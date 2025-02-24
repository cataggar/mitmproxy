import asyncio
import os
from mitmproxy import http, options
from mitmproxy.connection import Client, ConnectionState
from mitmproxy.addons import tlsconfig
from mitmproxy.proxy import events, context as proxy_context
from mitmproxy.proxy.layers import tcp, http
from mitmproxy.proxy.tunnel import LayerStack
from mitmproxy.test import taddons
from mitmproxy.proxy.layers import ServerTLSLayer

async def handle_event(handler, event):
    command_generator = handler._handle_event(event)
    for command in command_generator:
        print (f"Command: {command}")

async def main():
    # Set up options
    opts = options.Options()

    # Create a client connection
    client = Client(peername=("client", 1234), sockname=("127.0.0.1", 8080), timestamp_start=1605699329)
    client.state = ConnectionState.OPEN

    # Create a proxy context
    pctx = proxy_context.Context(client, opts)
    pctx.server.address = ("gcs.ppe.monitoring.core.windows.net", 443)

    # Set up TlsConfig addon
    tls_config = tlsconfig.TlsConfig()
    client_cert = os.path.expanduser('~/certs/gcs.ppe.monitoring.core.windows.net.pem')
    with taddons.context(tls_config, loadcore=True) as tctx:
        tctx.configure(tls_config, client_certs=client_cert)

        stack = LayerStack()
        stack /= tcp.TCPLayer(pctx)
        stack /= ServerTLSLayer(pctx)
        stack /= http.HttpLayer(pctx, http.HTTPMode.regular)

    start_event = events.Start()
    await handle_event(stack[0], start_event)
    
    request_bytes = b'GET /api/agent/v2/Test/SkyLink/MonitoringConfiguration/?Namespace=SkyLink&Version=Ver2v0.109&OSType=Linux HTTP/1.1\r\n'
    data_received_event = events.DataReceived(client, request_bytes)
    await handle_event(stack[0], data_received_event)

asyncio.run(main())