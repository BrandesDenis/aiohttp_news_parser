import re
import asyncio
import aiohttp
import bs4
from dataclasses import dataclass, field
from typing import List, Optional, Dict


DEFAULT_SITES = [
    "https://meduza.io/",
    "https://ria.ru/",
    "https://lenta.ru/",
    "https://www.rbc.ru/",
    "https://www.vesti.ru/",
    "https://russian.rt.com/",
]


@dataclass
class KeyWord:
    title: str

    def __post_init__(self):
        self.words = []

        for word in self.title.split("&"):
            self.words.append(word.lower().strip())

    def __str__(self):
        return self.title

    def entry(self, text: str) -> bool:
        return all(w in text for w in self.words)


@dataclass
class Scarper:
    key_words: List[str] = field(default_factory=list)
    sites: Optional[List[str]] = field(default_factory=list)

    def __post_init__(self):
        if not isinstance(self.sites, list) or not len(self.sites):
            self.sites = DEFAULT_SITES

        self._key_words = [KeyWord(k) for k in self.key_words]

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
        except aiohttp.ClientError:
            return entries

        main_page_text = main_page_text.lower()

        # проверим, есть ли вообще на сайте вхождения
        finded_kw = [kw for kw in self._key_words if kw.entry(main_page_text)]
        if not finded_kw:
            return entries

        parser = bs4.BeautifulSoup(main_page_text, "lxml")
        titles = parser.findAll(text=re.compile(".{10,}"))
        # оптимизировать цикл через регулярку
        for title in titles:
            for kw in finded_kw:
                if kw.entry(title):
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


async def get_sites_entries(
    key_words: List[str], sites: Optional[List[str]] = None
) -> List[Dict[str, str]]:

    sc = Scarper(key_words, sites)

    return await sc.get_entries()
