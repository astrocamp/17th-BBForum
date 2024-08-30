from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import PointsDetails, UserProfile, PointLog

def add_points(sender, instance, created, **kwargs):
    if created:
        # 當會員被創建時添加初始點數
        instance.points = 1
        instance.save()

@receiver(post_save, sender=PointsDetails)
def update_user_points(sender, instance, **kwargs):
    user_profile = UserProfile.objects.get(user=instance.user)
    
    if instance.action_type == 'login':
        # 获取当天的日期
        today = timezone.now().date()
        # 检查用户今天是否已经登录过
        if not PointsDetails.objects.filter(user=instance.user, action_type='login', actioned_at__date=today).exists():
            user_profile.points += instance.point_number
            user_profile.save()

    elif instance.action_type == 'post':
        # 检查当天的发文次数
        today = timezone.now().date()
        post_count = PointsDetails.objects.filter(user=instance.user, action_type='post', actioned_at__date=today).count()
        if post_count < 5:
            user_profile.points += instance.point_number
            user_profile.save()

    elif instance.action_type == 'like':
        if instance.point_number >= 100:
            user_profile.points += 10
            user_profile.save()

    elif instance.action_type == 'payment':
        user_profile.points += instance.point_number
        user_profile.save()

    elif instance.action_type == 'report':
        user_profile.points -= 2
        user_profile.save()

    # 记录日志
    PointLog.objects.create(user=user_profile, action=instance.action_type, points_change=instance.point_number)
