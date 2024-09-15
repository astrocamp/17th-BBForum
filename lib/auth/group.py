from django.contrib.auth.models import Group

from articles.models import Article
from follows.models import FollowRelation


def assign_user_to_group(user, post_count, follow_count):
    # 計算發文數和追蹤者數的綜合結果
    total_activity_count = (post_count // 10) + (follow_count // 20)
    group_name = f"LV.{total_activity_count}"
    group, created = Group.objects.get_or_create(name=group_name)
    user.groups.clear()
    user.groups.add(group)


# 將發文數和追蹤者數傳入
def update_user_group(user):
    follow_count = FollowRelation.objects.filter(follower=user).count()
    post_count = Article.objects.filter(user=user).count()
    assign_user_to_group(user, post_count, follow_count)
