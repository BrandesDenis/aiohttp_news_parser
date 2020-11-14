import re
import asyncio
import aiohttp
import bs4
from dataclasses import dataclass, field
from typing import Any, List, Optional, Dict


DEFAULT_SITES = [
    "https://meduza.io",
    "https://ria.ru",
    "https://lenta.ru",
    "https://www.rbc.ru",
    "https://www.vesti.ru",
    "https://russian.rt.com",
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
    entries: Dict[str, List[Dict[str, str]]] = field(default_factory=dict, init=False)

    def __post_init__(self):
        if not isinstance(self.sites, list) or not len(self.sites):
            self.sites = DEFAULT_SITES

        self._key_words = [KeyWord(k) for k in self.key_words]

    async def get_entries(self) -> List[Dict[str, Any]]:

        async with aiohttp.ClientSession() as session:
            futures = [self._find_site_entries(session, site) for site in self.sites]
            await asyncio.wait(futures)

        return [
            {"keyword": kw, "entries": entries} for kw, entries in self.entries.items()
        ]

    async def _find_site_entries(self, session: aiohttp.ClientSession, site: str):
        try:
            async with session.get(site) as response:
                response.raise_for_status()
                page_text = await response.text()
        except aiohttp.ClientError:
            return

        page_text = page_text.lower()

        # проверим, есть ли вообще на сайте вхождения
        finded_kw = [kw for kw in self._key_words if kw.entry(page_text)]
        if not finded_kw:
            return

        parser = bs4.BeautifulSoup(page_text, "lxml")
        # Ищем теги длиной от 10 символов, которые содержат искомые слова
        # и берем из них(или из родителей) ссылку href
        tags = parser.find_all(text=re.compile(".{10,}"))
        for tag in tags:
            for kw in finded_kw:
                if kw.entry(tag):
                    tag_ref = tag.find_parent(href=True)
                    if tag_ref is None:
                        continue
                    ref = tag_ref["href"]
                    if "http" not in ref:
                        ref = site + ref

                    keyword_entries = self.entries.setdefault(kw.title, [])
                    keyword_entries.append(
                        {
                            "ref": ref,
                            "title": str(tag),
                            "source": site,
                        }
                    )


async def get_sites_entries(
    key_words: List[str], sites: Optional[List[str]] = None
) -> List[Dict[str, Dict[str, str]]]:

    sc = Scarper(key_words, sites)

    return await sc.get_entries()
