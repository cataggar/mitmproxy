import os
from mitmproxy.tools.main import mitmproxy

os.environ['SSLKEYLOGFILE'] = os.path.expanduser('~/certs/key.log')
cert = os.path.expanduser('~/certs/gcs.ppe.monitoring.core.windows.net.pem')

# https://docs.mitmproxy.org/stable/concepts-options/
args = [
        "--set", "http2=false",
        "--set", f"client_certs={cert}",
        # "--set", "tls_version_server_max=TLS1_2",
        ]
mitmproxy(args)
