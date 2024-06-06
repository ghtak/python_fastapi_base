import uuid
from typing import Callable

from fastapi.routing import APIRoute
from starlette.requests import Request
from starlette.responses import Response

from core.app_context import AppContext


class LoggingRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            msg_id = str(uuid.uuid4())
            await self.log_request(msg_id, request)
            response = await original_route_handler(request)
            return await self.log_response(msg_id, request, response)

        return custom_route_handler

    @staticmethod
    async def log_request(msg_id: str, request: Request):
        extra = {
            'msg_id': msg_id,
            'method': request.method,
            'url': request.url,
            'header': request.headers,
            # 'url': request.url.path,
            # 'q_param': request.query_params,
            # 'p_param': request.path_params
        }
        if (
                request.method in ["POST", "PUT", "PATCH"]
                and "application/json" in request.headers.get("content-type")
        ):
            req_body = await request.body()
            extra['body'] = req_body

        AppContext.logger.info(f"req -- {','.join([f'{{{k}:{v}}}' for k, v in extra.items()])}", )

    @staticmethod
    async def log_response(msg_id: str, request: Request, response: Response) -> Response:
        extra = {
            'msg_id': msg_id,
            'method': request.method,
            'url': request.url,
        }
        if "application/json" in response.headers.get("content-type"):
            extra['body'] = response.body.decode("utf-8")

        # if isinstance(response, StreamingResponse):
        #     res_body = b''
        #     async for item in response.body_iterator:
        #         res_body += item
        #     extra['body'] = res_body.decode("utf-8")
        #     response = Response(content=res_body, status_code=response.status_code,
        #                         headers=dict(response.headers), media_type=response.media_type)
        # else:
        #     extra['body'] = response.body.decode("utf-8")

        AppContext.logger.info(f"res -- {','.join([f'{{{k}:{v}}}' for k, v in extra.items()])}", )
        return response
