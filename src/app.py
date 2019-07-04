from aiohttp import web
from src.controller.auth_controller import routes as auth_routes
from src.controller.client_controller import routes as client_routes

app = web.Application()
app.add_routes(auth_routes)
app.add_routes(client_routes)
web.run_app(app)
