from news_parser import views


def setup_routes(app):
    app.router.add_get("/", views.search_page)
    app.router.add_post("/api", views.api_get_entries)
