import re

from django import template

register = template.Library()


@register.filter
def should_include_nav_bar(request):
    url_name = getattr(request.resolver_match, "url_name", None)
    path = request.path
    print(path)
    if (
        url_name
        and url_name not in ["register", "sign_in", "auth_denied"]
        and path
        in [
            "/",
            "/my_watchlist/",
            "/my_favorites/",
            "/news_feed/",
            "/stock_market/",
            "/taiwan_futures/",
            "/popular_stocks/",
            "/popular_students/",
            "/popular_answers/",
            "/stock_notfound/",
        ]
        or re.match(r"^/stocks/.*", path)
    ):
        return True
    return False
