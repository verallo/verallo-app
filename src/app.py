from aiohttp import web
from src.controller.auth_controller import routes as auth_routes
from src.controller.account_controller import routes as client_routes
from src.controller.balance_controller import routes as balance_routes
from src.controller.transaction_controller import routes as transaction_routes

app = web.Application()
app.add_routes(auth_routes)
app.add_routes(client_routes)
app.add_routes(balance_routes)
app.add_routes(transaction_routes)
web.run_app(app)
