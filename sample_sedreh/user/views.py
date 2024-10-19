from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, ModelViewSet
from .models import User, OtpCode, Library
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema
from rest_framework import status
from .serializers import (
    UserEditSerializer,
    UserRegisterSerializer,
    OtpCodeSerializer,
    LibrarySerializer,
)


class ViewUserRegisteration(ViewSet):
    query_set = User.objects.all()
    # authentication_classes = [JWTAuthentication]
    # permission_classes = (IsAuthenticated, IsUser)

    def retrieve(self, request, pk=None):
        users = User.objects.filter(pk=pk)
        if users:
            ser_data = UserRegisterSerializer(users)
            return Response(ser_data.data)
        else:
            return Response(
                data={"user does not exist"}, status=status.HTTP_404_NOT_FOUND
            )

    # @action(detail=True, methods=["get"])
    def list(self, request):
        users = User.objects.all()
        ser_data = UserRegisterSerializer(users, many=True)
        return Response(ser_data.data)

    @extend_schema(
        request=UserRegisterSerializer,
        responses={201: UserRegisterSerializer},
        description="Endpoint for user registration",
    )
    def create(self, request):
        ser_data = UserRegisterSerializer(data=request.data)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=UserEditSerializer,
        responses={201: UserEditSerializer},
        description="Endpoint for user edit",
    )
    def update(self, request, pk=None):
        user = User.objects.get(pk=pk)
        ser_edit_data = UserEditSerializer(
            instance=user, data=request.data, partial=True
        )
        if ser_edit_data.is_valid():
            ser_edit_data.save()
            return Response(ser_edit_data.data, status=status.HTTP_200_OK)
        return Response(ser_edit_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        user = User.objects.get(pk=pk)
        user.delete()
        return Response({"meesages": "user deleted"}, status=status.HTTP_200_OK)


class LibraryView(ModelViewSet):
    queryset = Library.objects.all()
    serializer_class = LibrarySerializer
    permission_classes = []


class OtpCodeView(ModelViewSet):
    queryset = OtpCode.objects.all()
    serializer_class = OtpCodeSerializer
    permission_classes = []
