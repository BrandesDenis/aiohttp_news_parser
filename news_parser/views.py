import json

import aiohttp_jinja2
from aiohttp import web
from aiohttp_apispec import (
    docs,
    request_schema,
)

from news_parser.scarper import get_sites_entries, DEFAULT_SITES
from news_parser.schemas import EntriesRequest, EntriesResponse


@aiohttp_jinja2.template("index.html")
async def search_page(request):
    keywords = request.rel_url.query.get("keywords", "")

    if keywords:
        keywords = keywords.split(";")
        entries = await get_sites_entries(keywords)
    else:
        entries = []

    return {"entries": entries}


@docs(
    tags=["Методы"],
    summary="Получить статьи",
    description=f"""
    Метод для получения новостных статей по переданным ключевым словам.
    Если в метод передается список сайтов, то поиск выполняется по списку,
    иначе поиск выполняется в сайтах по умолчанию:
    {','.join(DEFAULT_SITES)}""",
    responses={
        200: {"description": "Ok", "schema": EntriesResponse},
        400: {"description": "Invalid JSON"},
    },
)
@request_schema(EntriesRequest)
async def api_get_entries(request):
    try:
        request_data = await request.json()
    except json.JSONDecodeError:
        return web.Response(status=400, text="Invalid JSON")

    keywords = request_data.get("keywords")
    sites = request_data.get("sites")

    if isinstance(keywords, list):
        entries = await get_sites_entries(keywords, sites)
    else:
        entries = []

    return web.json_response({"results": entries})
