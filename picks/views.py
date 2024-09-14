from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from articles.models import IndustryTag
from picks.models import UserStock


class PickStockAPI(APIView):
    def post(self, request, id):
        user = request.user

        industry_tag = IndustryTag.objects.get(security_code=id)
        _, created = UserStock.objects.get_or_create(user=user, stock=industry_tag)

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
        user = request.user

        try:
            pick = UserStock.objects.get(user=user, stock=id)
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
        user = request.user
        is_picked = UserStock.objects.filter(user=user, stock=id).exists()
        return Response({"is_picked": is_picked}, status=status.HTTP_200_OK)
