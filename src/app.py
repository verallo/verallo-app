import logging

from aiohttp import web

from src.controller.auth_controller import routes as auth_routes
from src.controller.account_controller import routes as client_routes
from src.controller.balance_controller import routes as balance_routes
from src.controller.transaction_controller import routes as transaction_routes

@web.middleware
async def error_middleware(request, handler):
    try:
        response = await handler(request)
    except ValueError as ve:
        return web.json_response({'code': 400, 'message': str(ve)})
    except TypeError as te:
        return web.json_response({'code': 500, 'message': str(te)})
    except Exception as e:
        return web.json_response({'code': 500, 'message': str(e)})
    return response


app = web.Application(middlewares=[error_middleware])
app.add_routes(auth_routes)
app.add_routes(client_routes)
app.add_routes(balance_routes)
app.add_routes(transaction_routes)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
web.run_app(app)
