from marshmallow import Schema, fields

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
