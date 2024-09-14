import logging

from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

from userprofiles.models import Profile

logger = logging.getLogger(__name__)


@receiver(user_logged_in)
def give_initial_points(sender, request, user, **kwargs):
    profile, created = Profile.objects.get_or_create(user=user)
    if created or profile.last_point_date is None:  # 如果是第一次登录或首次积分日期为空
        profile.tot_point += 1  # 初始积分1分
        profile.save()
    else:
        logger.info(
            f"Points not added for user {user.username} as profile already exists or already received today's points"
        )
