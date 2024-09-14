import json

from django.core.serializers.json import DjangoJSONEncoder

from userprofiles.models import Profile


def user_points(request):
    if request.user.is_authenticated:
        tot_point = request.session.get("points")
        if tot_point is None:
            profile = Profile.objects.get(user=request.user)
            tot_point = profile.tot_point
            request.session["points"] = json.dumps(tot_point, cls=DjangoJSONEncoder)
        else:
            tot_point = int(tot_point.strip('"'))
        return {"tot_point": tot_point}
    return {"tot_point": 0}
