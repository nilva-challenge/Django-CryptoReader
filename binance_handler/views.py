from rest_framework.generics import GenericAPIView
from .utils import binance_api_list_of_open_positions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class OpenPositions(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        response = binance_api_list_of_open_positions(user.binance_key, user.binance_secret)
        return Response(response)