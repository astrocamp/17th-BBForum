from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def should_include_nav_bar(context):
    request = context["request"]
    url_name = getattr(request.resolver_match, "url_name", None)
    path = request.path
    if (
        url_name
        and url_name not in ["register", "sign_in", "auth_denied"]
        and path
        in [
            "/",
            "/my_watchlist/",
            "/my_favorites/",
            "/news_feed/",
            "/market_index/",
            "/taiwan_index/",
            "/popular_stocks/",
            "/popular_students/",
            "/popular_answers/",
        ]
    ):
        return True
    return False
