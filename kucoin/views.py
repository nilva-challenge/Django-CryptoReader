from rest_framework.generics import GenericAPIView
from .utils import kucoin_api
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class OpenPositions(GenericAPIView):
    '''
        Get and view open (active) positions. 
    '''

    permission_classes = (IsAuthenticated,)

    def get(self, request) -> Response:
        user = request.user
        status, response = kucoin_api(user.kucoin_key, user.kucoin_secret,
                                      user.kucoin_passphrase, '/api/v1/orders', 'status=active')

        return Response(response, status=status)
