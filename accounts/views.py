from rest_framework import status
from rest_framework.generics import CreateAPIView
from .serializers import RegisterSerializer
from rest_framework.response import Response


class Register(CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"message": "Account created successfully."}, status=status.HTTP_201_CREATED)
