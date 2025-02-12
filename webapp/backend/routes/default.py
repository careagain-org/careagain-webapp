from fastapi import APIRouter
from starlette.responses import RedirectResponse

default = APIRouter()

@default.get('/')
def default_route():
    return RedirectResponse(url="/docs")

# @default.get('/ping/')
# def default_route():
#     return "pong"

# @default.get('/_event')
# def default_route():
#     return "The client is using an unsupported version of the Socket.IO or Engine.IO protocols"