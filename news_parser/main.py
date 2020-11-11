from pathlib import Path

import aiohttp_jinja2
import jinja2
from aiohttp import web

from routes import setup_routes


BASE_DIR = Path(__file__).resolve().parent.parent


app = web.Application()
aiohttp_jinja2.setup(
    app,
    loader=jinja2.FileSystemLoader(str(BASE_DIR / "news_parser" / "templates")),
)
setup_routes(app)

web.run_app(app)
