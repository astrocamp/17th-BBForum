from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from articles.models import IndustryTag
from picks.models import UserStock


class PickStockAPI(APIView):
    def post(self, request, id):
        picker = request.user
        print("-------------------")
        print(picker)
        print(id)

        industry_tag = IndustryTag.objects.get(security_code=id)
        print(industry_tag)

        _, created = UserStock.objects.get_or_create(user=picker, stock=industry_tag)

        if created:
            return Response(
                {"message": f"You are now pick {id}"},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"message": f"You are already pick {id}"},
                status=status.HTTP_200_OK,
            )

    def delete(self, request, id, *args, **kwargs):
        picker = request.user

        try:
            pick = UserStock.objects.get(user=picker, stock=id)
            pick.delete()
            return Response(
                {"message": f"You have unpick {id}"},
                status=status.HTTP_200_OK,
            )
        except UserStock.DoesNotExist:
            return Response(
                {"message": "You are not pick this stock"},
                status=status.HTTP_404_NOT_FOUND,
            )


class CheckPickStatusAPI(APIView):
    def get(self, request, id):
        # picker = request.user

        # try:
        #     following = User.objects.get(id=id)
        # except User.DoesNotExist:
        #     return Response(
        #         {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
        #     )

        # is_following = UserStock.objects.filter(
        #     follower=follower, following=following
        # ).exists()

        # return Response({"is_following": is_following})
        return Response()
