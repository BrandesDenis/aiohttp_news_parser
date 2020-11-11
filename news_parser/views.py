import aiohttp_jinja2
from scarper import get_sites_entries


@aiohttp_jinja2.template("index.html")
async def index(request):
    keywords = request.rel_url.query.get("keywords", "")

    keywords = keywords.split(";")
    entries = await get_sites_entries(keywords)

    return {"entries": entries}
