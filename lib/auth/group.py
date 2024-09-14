from django.contrib.auth.models import Group

from articles.models import Article
from follows.models import FollowRelation


def assign_user_to_group(user, post_count, follow_count):
    # 計算發文數和追蹤者數的綜合結果
    total_activity_count = (post_count // 10) + (follow_count // 10)
    group_name = f"LV.{total_activity_count}"

    # 檢查用户是否已經在比當前 group 更高級的群組
    current_groups = user.groups.all()
    highest_group_level = max(
        [
            int(group.name.split(".")[1])
            for group in current_groups
            if group.name.startswith("LV.")
        ],
        default=0,
    )

    # 如果當前計算的階級更高，則升級群組
    if total_activity_count > highest_group_level:
        group, created = Group.objects.get_or_create(name=group_name)
        user.groups.clear()
        user.groups.add(group)


# 將發文數和追蹤者數傳入
def update_user_group(user):
    post_count = Article.objects.filter(user=user).count()
    follow_count = FollowRelation.objects.filter(following=user).count()
    assign_user_to_group(user, post_count, follow_count)
