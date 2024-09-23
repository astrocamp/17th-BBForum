from django.conf import settings


def current_user_groups(request):
    if request.user.is_authenticated:
        user_groups = request.user.groups.values_list("name", flat=True)
        return {"current_user_groups": user_groups}
    return {}
