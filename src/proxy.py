import secrets

from fastapi import FastAPI, Request, Response
from furl import furl
import httpx

import config
import helpers
from logs import log_error, log_request, log_response

app = FastAPI()
pools = helpers.build_pools_set()


@app.api_route("/{path_str:path}", methods=config.METHODS)
async def proxy(request: Request, path_str: str):
    request_id = secrets.token_hex(8)
    request_headers = dict(request.headers)
    request_url = request.url
    request_method = request.method
    request_body = await request.body()
    request_cookies = request.cookies
    log_string = f"{request_id} | {request_method} | {request_url}"
    pool_id_header_name = config.POOL_ID_HEADER.lower()

    # if pool_id_header_name not in request_headers:
    #     log_error(f"{log_string} | Pool ID header is missing")
    #     return Response(
    #         status_code=400,
    #         headers={config.REQUEST_ID_HEADER: request_id},
    #         content=f"{config.POOL_ID_HEADER} header is missing",
    #     )
    #
    # pool_id = request_headers[pool_id_header_name]
    # del request_headers[pool_id_header_name]
    #
    # if pool_id not in pools:
    #     log_error(f"{log_string} | Unknown Pool ID: {pool_id}")
    #     return Response(
    #         status_code=404,
    #         headers={config.REQUEST_ID_HEADER: request_id},
    #         content="Unknown Pool ID",
    #     )
    #
    # log_request(
    #     f"{log_string} | {pool_id} | {request_headers} | {request_body.decode()} | {request_cookies}"
    # )

    # target = secrets.choice(pools[pool_id])
    target = secrets.choice(pools["pool-json"])
    redirect_furl = furl(request_url)
    redirect_furl.scheme = target[0]
    redirect_furl.host = target[1]
    redirect_furl.port = target[2]
    redirect_url = redirect_furl.url
    log_string = f"{request_id} | {request_method} | {redirect_url}"

    async with httpx.AsyncClient() as client:
        try:
            proxy_response = await client.request(
                method=request_method,
                url=redirect_url,
                headers=request_headers,
                content=request_body,
                cookies=request_cookies,
                timeout=config.TIMEOUT,
            )

            proxy_headers = dict(proxy_response.headers)
            proxy_headers[config.REQUEST_ID_HEADER] = request_id
            proxy_body = proxy_response.content
            proxy_status_code = proxy_response.status_code
            log_response(
                f"{log_string} | {proxy_status_code} | {proxy_headers} | {proxy_body}"
            )
            return Response(
                status_code=proxy_status_code, content=proxy_body, headers=proxy_headers
            )
        except (httpx.ConnectError, httpx.ConnectTimeout):
            log_error(f"{log_string} | Connection error")
            return Response(
                status_code=408,
                headers={config.REQUEST_ID_HEADER: request_id},
                content="Connection error",
            )
