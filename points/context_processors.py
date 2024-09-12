from userprofiles.models import Profile


def user_points(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        return {"tot_point": profile.tot_point}
    return {"tot_point": 0}
