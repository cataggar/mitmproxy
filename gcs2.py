import os
from mitmproxy.tools.main import mitmproxy

# https://docs.mitmproxy.org/stable/concepts-options/

os.environ['SSLKEYLOGFILE'] = os.path.expanduser('~/certs/key.log')
cert = os.path.expanduser('~/certs/gcs.ppe.monitoring.core.windows.net.pem')

args = ["--set", "http2=false",
        "--set", f"client_certs={cert}",
        "--set", "tls_version_client_min=TLS1_2",
        "--set", "tls_version_server_min=TLS1_2",
        "--set", "tls_version_client_max=TLS1_2",
        "--set", "tls_version_server_max=TLS1_2",
        # "--set", "proxy_debug=true",
        # "--set", "console_eventlog_verbosity=debug",
        ]
mitmproxy(args)
