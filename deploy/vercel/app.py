"""Vercel entry point for the upstream stateless HTTP MCP transport."""

import os

from librus_mcp.config import ConfigError, load_config
from librus_mcp.http_transport import (
    MAX_REQUEST_BODY_BYTES,
    BearerTokenMiddleware,
    load_token,
    transport_security,
)
from librus_mcp.server import create_server
from starlette.responses import JSONResponse


def build_app():
    hostname = os.environ.get("VERCEL_PROJECT_PRODUCTION_URL")
    required = ("LIBRUS_USERNAME", "LIBRUS_PASSWORD", "LIBRUS_CONTEXT_KEY")
    if not hostname or not all(os.environ.get(name) for name in required):
        return unavailable
    os.environ["LIBRUS_FEATURES"] = (
        '{"attachments":false,"notifications":false,'
        '"send_message":false,"mark_read_consent":true}'
    )
    try:
        token = load_token()
        config = load_config(None)
    except ConfigError:
        return unavailable
    server = create_server(config)
    mcp = server.streamable_http_app(
        stateless_http=True,
        json_response=True,
        max_request_body_size=MAX_REQUEST_BODY_BYTES,
        transport_security=transport_security(hostname, [hostname]),
        host=hostname,
    )
    return BearerTokenMiddleware(mcp, token)


async def unavailable(scope, receive, send):
    if scope["type"] == "lifespan":
        await receive()
        await send({"type": "lifespan.startup.complete"})
        await receive()
        await send({"type": "lifespan.shutdown.complete"})
        return
    await JSONResponse({"error": "MCP not configured"}, status_code=503)(
        scope, receive, send
    )


app = build_app()
