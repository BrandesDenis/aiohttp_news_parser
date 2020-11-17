import pytest

from news_parser.main import get_app


class MockResponse:
    def __init__(self, text, status=200):
        self._text = text
        self.status = status

    async def text(self):
        return self._text

    def raise_for_status(self):
        pass

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def __aenter__(self):
        return self


@pytest.fixture
def get_site_html_mock(*args, **kwargs):
    return lambda *args, **kwargs: MockResponse(
        text="""
    <!doctype html>
        <body>
            <div class="mx-3">
                <p>
                    <a href="test.test">test 1</a>
                <p>
                <p>
                    <a href="test2.test">TEST 2</a>
                <p>
                <p>
                    <a href="test3.test"> t_e_s_t 1</a>
                <p>
                <p>
                    <a href="test4.test"> t_e_s_t 2</a>
                <p>
            </div>
    </body>
    """
    )


@pytest.fixture
def cli(loop, aiohttp_client):
    app = get_app()
    return loop.run_until_complete(aiohttp_client(app))
