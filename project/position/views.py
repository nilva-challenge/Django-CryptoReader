from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Position
from .serializers import PositionSerializer, TrackingPositionSerializer
from project.api_utility import Utility


class PositionTrackingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # code to start position tracking for the authenticated user
        user = request.user

        serializer = TrackingPositionSerializer(data=Utility(user=user).output,
                                                context={'user_id': user.pk})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
        # return Response({'detail': 'Position tracking started.'})


class OpenPositionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        positions = Position.objects.filter(user=user)
        serializer = PositionSerializer(positions, many=True)
        return Response(serializer.data)
