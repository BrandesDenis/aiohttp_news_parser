from unittest.mock import patch


async def test_api_get(cli):
    resp = await cli.get("/api")

    assert resp.status == 405


async def test_api_post(cli, get_site_html_mock):
    with patch("aiohttp.ClientSession.get", get_site_html_mock):

        resp = await cli.post(
            "/api", json={"keywords": ["test"], "sites": ["test.test"]}
        )

        text = await resp.text()
        print(text)
        assert resp.status == 200


async def test_api_post_empty(cli):
    resp = await cli.post("/api")

    assert resp.status == 400


async def test_search_page_empty(cli):
    resp = await cli.get("/")

    assert resp.status == 200


async def test_search_page(cli, get_site_html_mock):
    with patch("aiohttp.ClientSession.get", get_site_html_mock):
        resp = await cli.get("/?keywords=test")

        assert resp.status == 200
