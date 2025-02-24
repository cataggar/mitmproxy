import asyncio
import os
from mitmproxy import http, options, certs, connection, tls, proxy
from mitmproxy.connection import Client, ConnectionState
from mitmproxy.options import Options
from mitmproxy.addonmanager import Loader
from mitmproxy.addons import tlsconfig
from mitmproxy.proxy import commands, events, context as proxy_context
from mitmproxy.master import Master
from mitmproxy.proxy.layers.http._http1 import Http1Server
from mitmproxy.proxy.layers import tcp, http
from mitmproxy.proxy.tunnel import LayerStack
from mitmproxy.tcp import TCPFlow
from mitmproxy.test import taddons
import pprint
from mitmproxy.proxy.layers import TCPLayer, ServerTLSLayer
from mitmproxy.http import Request
from test.mitmproxy.proxy import tutils

async def execute_command(command):
    if isinstance(command, commands.SendData):
        print(f"- SendData: {command.data}")
    elif isinstance(command, commands.CloseConnection):
        print(f"- CloseConnection: {command.connection}")
    elif isinstance(command, commands.Log):
        print(f"- Log: {command.message}")
    else:
        print(f"* Unhandled command: {command}")

async def handle_event(handler, event):
    command_generator = handler._handle_event(event)
    for command in command_generator:
        await execute_command(command)

async def get_monitoring_config():
    pp = pprint.PrettyPrinter(indent=2)
    # client_cert = os.path.expanduser('~/certs/gcs.ppe.monitoring.core.windows.net.pem')
    # with open(client_cert, "rb") as f:
    #     client_cert_bytes = f.read()
    # cert = certs.Cert.from_pem(client_cert_bytes)

    # server = connection.Server(address=("gcs.ppe.monitoring.core.windows.net", 443), certificate_list=[cert])
    
    # opts = options.Options()
    # mitmproxy_ctx.options = opts

    # master = Master(opts)
    # loader = Loader(master)

    
    # options = Options()

    # ta = tlsconfig.TlsConfig()
    # with taddons.context(ta, loadcore=False) as actx:
        # a = tctx.master.addons
        # a.add(tlsconfig.TlsConfig())

        # get TlsConfig from addons
        # a.lookup("tlsconfig").load(tctx)

        # options = options.Options()

        #a._configure_all(tctx.options)
        # tcfg = a.get("tlsconfig")
        # actx.configure(
        #     ta,
        #     client_certs=client_cert,
        # )

        # server = Http1Server(tctx)
        # server.

        # pctx = proxy_context.Context(
        #     # server=connection.Server(address=("gcs.ppe.monitoring.core.windows.net", 443)),
        #     connection.Client(
        #         peername=("client", 1234),
        #         sockname=("127.0.0.1", 8080),
        #         timestamp_start=1605699329,
        #     ),
        #     options,
        # )
        # pctx.server.address = ("gcs.ppe.monitoring.core.windows.net", 443)
        
        # http1_server = Http1Server(pctx)
        
        # # Handle the Start event
        # start_event = events.Start()
        # await handle_event(http1_server, start_event)

        # # Handle a DataReceived event
        # data_received_event = events.DataReceived(client, b"GET / HTTP/1.1\r\nHost: example.com\r\n\r\n")
        # await handle_event(http1_server, data_received_event)

        # # Handle a ConnectionClosed event
        # connection_closed_event = events.ConnectionClosed(client)
        # await handle_event(http1_server, connection_closed_event)


        # t = tcp.TCPLayer(pctx)
        # x1 = t.handle_event(events.Start())
        # pp.pprint(f"x1: {x1}")
        # x2 = commands.OpenConnection(pctx.server)
        # pp.pprint(f"x2: {x2}")
        # x3 = t.handle_event(x2)
        # pp.pprint(f"x3: {x3}")
        # pp.pprint(pctx.server.connected)
        # pp.pprint(pctx.server.tls_established)
        # assert x1 == [commands.OpenConnection(pctx.server)]

        # ctx = context.Context(
        #     connection.Client(
        #         peername=("client", 1234),
        #         sockname=("127.0.0.1", 8080),
        #         timestamp_start=1605699329,
        #     ),
        #     tctx.options,
        # )

        # ctx.server.address = ('gcs.ppe.monitoring.core.windows.net', 443)
        # ctx.server.sni = ""  # explicitly opt out of using the address.

        # tls_start = tls.TlsData(ctx.server, context=ctx)
        # ta.tls_start_server(tls_start)

        # print(f"connected: {ctx.server.connected}")
        # pp.pprint(ctx.server.__dict__)

        # pp.pprint(ta)
        

        # loader = tctx.master.loader
        # tls_start = tls.TlsData(server, tctx)
        # tcfg = tlsconfig.TlsConfig()
        # tcfg.load(loader)

        # tcfg.tls_start_server(tls_start)

    # connection = SSL.Connection(context, socket.socket(socket.AF_INET, socket.SOCK_STREAM))
    # connection.connect(('gcs.ppe.monitoring.core.windows.net', 443))
    # connection = tls_start.ssl_conn

    # request = (
    #     b'GET /api/agent/v2/Test/SkyLink/MonitoringConfiguration/?Namespace=SkyLink&Version=Ver2v0.109&OSType=Linux HTTP/1.1\r\n'
    #     b'Host: gcs.ppe.monitoring.core.windows.net\r\n\n'
    # )
    # tls_start.ssl_conn.send(request)

    # res_buf_size = 1024
    # response = b''
    # while True:
    #     data = tls_start.ssl_conn.recv(res_buf_size)
    #     response += data
    #     if len(data) < res_buf_size:
    #         break
    # tls_start.ssl_conn.shutdown()
    # tls_start.ssl_conn.close()
    # return response
    return None

# async def main():
    # response = await get_monitoring_config()
    # print(response)

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
        # tls_start = tls.TlsData(pctx.server, context=pctx)
        # tls_config.tls_start_server(tls_start)

        # Create an instance of LayerStack
        stack = LayerStack()

        # Add layers to the stack
        stack /= tcp.TCPLayer(pctx)
        stack /= ServerTLSLayer(pctx)
        stack /= http.HttpLayer(pctx, http.HTTPMode.regular)


    # Create an instance of Http1Server
    # http1_server = Http1Server(pctx)

    # Handle the Start event
    start_event = events.Start()
    await handle_event(stack[0], start_event)
    


    # Create an HTTP request
    # request = Request.make(
    #     method="GET",
    #     url="https://gcs.ppe.monitoring.core.windows.net/api/agent/v2/Test/SkyLink/MonitoringConfiguration/?Namespace=SkyLink&Version=Ver2v0.109&OSType=Linux",
    #     headers={
    #         "Host": "gcs.ppe.monitoring.core.windows.net"
    #     }
    # )
    # may be http1.assembly_request(request)

    # Handle a DataReceived event
    request_bytes = b'GET /api/agent/v2/Test/SkyLink/MonitoringConfiguration/?Namespace=SkyLink&Version=Ver2v0.109&OSType=Linux HTTP/1.1\r\n'
    data_received_event = events.DataReceived(client, request_bytes)
    await handle_event(stack[0], data_received_event)


    # http1_server.send

    # Handle a ConnectionClosed event
    # connection_closed_event = events.ConnectionClosed(client)
    # await handle_event(stack[0], connection_closed_event)

    # flow = tutils.Placeholder(TCPFlow)
    # unset flow.messages
    # playbook = tutils.Playbook(stack[0])
    # assert (
    #     playbook
    #     >> events.Start()
    #     << tcp.TcpStartHook(flow)
    #     << commands.OpenConnection(pctx.server)
    #     >> tutils.reply(None)
        # << events.DataReceived(client, request_bytes)
        # >> tutils.reply_next_layer(http.HttpLayer)
        # << commands.SendData(pctx.server, request_bytes)
        # << events.ConnectionClosed(client)
        # >> tutils.reply(None)
    # )


asyncio.run(main())