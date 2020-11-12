import json

import aiohttp_jinja2
from aiohttp import web

from scarper import get_sites_entries


@aiohttp_jinja2.template("index.html")
async def search_page(request):
    keywords = request.rel_url.query.get("keywords", "")

    if keywords:
        keywords = keywords.split(";")
        entries = await get_sites_entries(keywords)
    else:
        entries = []

    return {"entries": entries}


async def api_get_entries(request):
    """
    на вход данные вида:
    {
        'sites': ['site1', 'site2'],
        'keywords': ['word1', 'word2']
    }

    результат:
    {
        results:[
            {
                'word': ['ref1', 'ref2']
            }
        ]
    }

    мб пидантик или маршмаллоу?
    валидация
    автодокументация апи
    """

    try:
        request_data = await request.json()
    except json.JSONDecodeError:
        return web.Response(status=400, text='Invalid JSON')


    keywords = request_data.get("keywords")
    sites = request_data.get("sites")

    if isinstance(keywords, list):
        entries = await get_sites_entries(keywords, sites)
    else:
        entries = []

    return web.json_response({"results": entries})
