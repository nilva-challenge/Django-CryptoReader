from rest_framework.generics import CreateAPIView
from .serializers import RegisterSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


class Register(CreateAPIView):
    '''
        Signup users with given fields.
    '''

    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    def create(self, request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"message": "Account created successfully."}, status=201)
