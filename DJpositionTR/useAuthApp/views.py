from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken




@api_view(['GET'])  # Specify the HTTP methods allowed for this view
@permission_classes([IsAuthenticated])  # Set the permission classes
def my_view(request):
    # Your view logic here
    return Response("Authenticated user can access this view.")



class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):  
        try:               
            refresh_token = request.data["refresh_token"]               
            token = RefreshToken(refresh_token)               
            token.blacklist()               
            return Response(status=status.HTTP_205_RESET_CONTENT)          
        except Exception as e:               
            return Response(status=status.HTTP_400_BAD_REQUEST)