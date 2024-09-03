from django.contrib.auth.models import Group


def assign_user_to_group(user, post_count):
    group_level = post_count // 2
    group_name = f"LV.{group_level}"
    # 確保用户不在任何更高的 group 里
    user.groups.clear()  # 清空當前的组
    group, created = Group.objects.get_or_create(name=group_name)
    user.groups.add(group)