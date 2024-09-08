from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from userprofiles.models import Profile
import logging
from django.utils import timezone

logger = logging.getLogger(__name__)

class SoftDeleteBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        logger.info(f"Authenticating user: {username}")
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(username=username)
            profile = Profile.objects.get(user=user)
            logger.info(f"Profile deleted_at: {profile.deleted_at}")
            if profile.deleted_at is not None and profile.deleted_at <= timezone.now():
                logger.info(f"User {username} is soft deleted and cannot login.")
                return None  # 用戶已被軟刪除
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            logger.info(f"User {username} does not exist.")
            return None
        except Profile.DoesNotExist:
            logger.info(f"Profile for user {username} does not exist.")
            return None
        return None
