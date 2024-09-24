from django.shortcuts import get_object_or_404

from userprofiles.models import Profile


def user_img_processor(request):
    user_img = None
    if request.user.is_authenticated:
        profile = get_object_or_404(Profile, user=request.user)
        user_img = profile.user_img
    return {
        "user_img": user_img,
    }
