from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class PickStockAPI(APIView):
    def post(self, request, id):
        follower = request.user

        try:
            following = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if follower == following:
            return Response(
                {"error": "You cannot follow yourself"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # _, created = FollowRelation.objects.get_or_create(
        #     follower=follower, following=following
        # )

        # if created:
        #     return Response(
        #         {"message": f"You are now following {following.username}"},
        #         status=status.HTTP_201_CREATED,
        #     )
        # else:
        #     return Response(
        #         {"message": f"You are already following {following.username}"},
        #         status=status.HTTP_200_OK,
        #     )

    def delete(self, request, id, *args, **kwargs):
        follower = request.user

        try:
            following = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # try:
        #     follow = FollowRelation.objects.get(follower=follower, following=following)
        #     follow.delete()
        #     return Response(
        #         {"message": f"You have unfollowed {following.username}"},
        #         status=status.HTTP_200_OK,
        #     )
        # except FollowRelation.DoesNotExist:
        #     return Response(
        #         {"message": "You are not following this user"},
        #         status=status.HTTP_404_NOT_FOUND,
        #     )


class CheckFollowStatusAPI(APIView):
    def get(self, request, id):
        follower = request.user

        try:
            following = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # is_following = FollowRelation.objects.filter(
        #     follower=follower, following=following
        # ).exists()

        # return Response({"is_following": is_following})
        return Response()
