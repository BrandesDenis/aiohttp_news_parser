import asyncio

from unittest.mock import patch

from news_parser.scarper import get_sites_entries


def test_scarper(get_site_html_mock):
    with patch("aiohttp.ClientSession.get", get_site_html_mock):

        test_keywords = ["test", "t_est"]

        test_sites = ["test.com"]

        res = asyncio.run(get_sites_entries(test_keywords, test_sites))

        control_res = [
            {
                "keyword": "test",
                "entries": [
                    {
                        "ref": "test.comtest.test",
                        "title": "test 1",
                        "source": "test.com",
                    },
                    {
                        "ref": "test.comtest2.test",
                        "title": "test 2",
                        "source": "test.com",
                    },
                ],
            }
        ]

        assert res == control_res


def test_scarper_empty_keywords(get_site_html_mock):
    with patch("aiohttp.ClientSession.get", get_site_html_mock):
        test_keywords = []
        test_sites = ["test.com"]

        res = asyncio.run(get_sites_entries(test_keywords, test_sites))

        control_res = []

        assert res == control_res


def test_scarper_empty_sites(get_site_html_mock):
    with patch("aiohttp.ClientSession.get", get_site_html_mock):
        test_keywords = ["test", "t_est"]

        res = asyncio.run(get_sites_entries(test_keywords))

        assert len(res) == 1
