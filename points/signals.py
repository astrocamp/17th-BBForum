from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

from userprofiles.models import Profile


@receiver(user_logged_in)
def give_initial_points(sender, request, user, **kwargs):
    profile, created = Profile.objects.get_or_create(user=user)
    if created or profile.last_point_date is None:
        profile.tot_point += 1
        profile.save()
