from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from .models import UserProfile, PointsDetails, PointLog

class PointSystemTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.user_profile, created = UserProfile.objects.get_or_create(user=self.user)

    def test_login_points(self):
        # 測試首次登入
        PointsDetails.objects.create(user=self.user, action_type='login', point_number=1)
        self.assertEqual(self.user_profile.points, 1)

        # 測試同一天再次登入
        PointsDetails.objects.create(user=self.user, action_type='login', point_number=1)
        self.assertEqual(self.user_profile.points, 1)  # 積分應該保持不變

    def test_post_points(self):
        # 測試發文積分
        for i in range(6):
            PointsDetails.objects.create(user=self.user, action_type='post', point_number=2)
        
        self.assertEqual(self.user_profile.points, 10)  # 應該只獲得10點（5篇文章各2點）

        # 再發一篇文章，確保不再增加積分
        PointsDetails.objects.create(user=self.user, action_type='post', point_number=2)
        self.assertEqual(self.user_profile.points, 10)  # 積分應該保持不變

    def test_like_received_points(self):
        # 測試收到100個讚
        for i in range(100):
            PointsDetails.objects.create(user=self.user, action_type='like_received', point_number=1)
        
        self.assertEqual(self.user_profile.points, 10)  # 應該獲得10點

    def test_reported_points(self):
        # 先給用戶一些積分
        self.user_profile.points = 5
        self.user_profile.save()

        # 測試被檢舉
        PointsDetails.objects.create(user=self.user, action_type='reported', point_number=-2)
        self.assertEqual(self.user_profile.points, 3)  # 應該扣除2點

        # 再次被檢舉
        PointsDetails.objects.create(user=self.user, action_type='reported', point_number=-2)
        self.assertEqual(self.user_profile.points, 1)  # 應該再扣除2點

        # 第三次被檢舉
        PointsDetails.objects.create(user=self.user, action_type='reported', point_number=-2)
        self.assertEqual(self.user_profile.points, 0)  # 積分不應該為負數

    def test_point_log_creation(self):
        # 測試 PointLog 是否正確創建
        PointsDetails.objects.create(user=self.user, action_type='login', point_number=1)
        log = PointLog.objects.last()
        self.assertEqual(log.user, self.user_profile)
        self.assertEqual(log.action, "login")
        self.assertEqual(log.points_change, 1)
