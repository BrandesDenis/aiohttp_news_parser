from marshmallow import Schema, fields


class EntriesRequest(Schema):
    keywords = fields.List(fields.Str(), description="Ключевые слова")
    sites = fields.List(fields.Str(), description="Сайты для поиска")


class KeywordsEntries(Schema):
    keyword = fields.Str(description="Ключевое слово")
    entries = fields.List(fields.Str(), description="Ссылки на статьи с вхождениями")


class EntriesResponse(Schema):
    results = fields.List(
        fields.Nested(KeywordsEntries),
        description="Списов вхождений по ключевым словам",
    )
