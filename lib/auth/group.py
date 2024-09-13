from django.contrib.auth.models import Group


def assign_user_to_group(user, post_count):
    group_level = post_count // 2
    group_name = f"LV.{group_level}"
    user.groups.clear()
    group, created = Group.objects.get_or_create(name=group_name)
    user.groups.add(group)
