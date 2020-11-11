import re
import asyncio
import aiohttp
import bs4
from dataclasses import dataclass, field
from typing import List, Optional, Dict


@dataclass
class Scarper:
    key_words: List[str] = field(default_factory=list)
    sites: Optional[List[str]] = field(default_factory=list)

    def __post_init__(self):
        if not isinstance(self.sites, list) or not len(self.sites):
            self.sites = _get_default_sites()

        self.key_words = [kw.lower().strip() for kw in self.key_words]

    async def get_entries(self) -> List[Dict[str, str]]:
        entries: List[Dict[str, str]] = []

        async with aiohttp.ClientSession() as session:
            futures = [self._get_site_entries(session, site) for site in self.sites]

            for future in asyncio.as_completed(futures):
                result = await future
                entries += result

        return entries

    async def _get_site_entries(
        self, session: aiohttp.ClientSession, site: str
    ) -> List[Dict[str, str]]:

        entries: List[Dict[str, str]] = []

        try:
            async with session.get(site) as response:
                response.raise_for_status()
                main_page_text = await response.text()
        except (aiohttp.ClientConnectionError, aiohttp.ClientResponseError):
            return entries

        main_page_text = main_page_text.lower()

        # проверим, есть ли вообще на сайте вхождения
        finded_kw = [w for w in self.key_words if w in main_page_text]
        if not finded_kw:
            return entries

        parser = bs4.BeautifulSoup(main_page_text, "lxml")
        titles = parser.findAll(text=re.compile(".{10,}"))
        # оптимизировать цикл через регулярку
        for title in titles:
            for kw in finded_kw:
                if kw in title.lower():
                    title_ref_block = title.findParent(href=True)
                    if title_ref_block is None:
                        continue
                    title_ref = title_ref_block["href"]
                    if "http" not in title_ref:
                        title_ref = site + title_ref

                    entries.append(
                        (
                            {
                                "ref": title_ref,
                                "title": title,
                                "source": site,
                            }
                        )
                    )

        return entries


def _get_default_sites():
    return [
        "https://meduza.io/",
        "https://ria.ru/",
        "https://lenta.ru/",
        "https://www.rbc.ru/",
        "https://www.vesti.ru/",
        "https://russian.rt.com/",
    ]


async def get_sites_entries(
    key_words: List[str], sites: Optional[List[str]] = None
) -> List[Dict[str, str]]:

    sc = Scarper(key_words, sites)

    return await sc.get_entries()
