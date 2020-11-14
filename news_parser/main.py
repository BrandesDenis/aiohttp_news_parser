from pathlib import Path

import aiohttp_jinja2
import jinja2
from aiohttp import web
from aiohttp_apispec import setup_aiohttp_apispec

from routes import setup_routes

BASE_DIR = Path(__file__).resolve().parent.parent


app = web.Application()
aiohttp_jinja2.setup(
    app,
    loader=jinja2.FileSystemLoader(str(BASE_DIR / "news_parser" / "templates")),
)

title = "Сервис для поиска новостей по ключевым словам"

setup_aiohttp_apispec(app=app, swagger_path="/api/doc", title=title, version="v1")

setup_routes(app)

web.run_app(app)
