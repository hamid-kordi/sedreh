from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, ModelViewSet
from .models import User, OtpCode, Library
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from .serializers import (
    UserEditSerializer,
    UserRegisterSerializer,
    OtpCodeSerializer,
    LibrarySerializer,
    IncreaseBudgetSerializer,
    BuyBookSerializer,
    RuternSerializer,
)
from .tasks import celery_buy_book, celery_increaseـtheـbudget, celery_return_book
from rest_framework.views import APIView


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


class BudgetManage(ViewSet):
    @extend_schema(
        request=IncreaseBudgetSerializer,
        responses={202: OpenApiResponse},
        description="Increase the user's budget using OTP code.",
    )
    @action(detail=False, methods=["post"])
    def increaseـtheـbudget(self, request):
        username = request.data.get("username")
        code = request.data.get("code")
        if username and code:
            task = celery_increaseـtheـbudget(username, code)
            return Response({"task_id": task.id}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(
                {"error": "username and code is necassery"},
                status=status.HTTP_404_NOT_FOUND,
            )

    @extend_schema(
        request=BuyBookSerializer,
        responses={202: OpenApiResponse},
        description="buy book for users",
    )
    @action(detail=False, methods=["post"])
    def buy_book(self, request):
        username = request.data.get("username")
        book_id = request.data.get("book_id")
        if username and book_id:
            task = celery_buy_book.delay(username, book_id)
            return Response({"task_id": task.id}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(
                {"error": "username and book_id is necassery"},
                status=status.HTTP_404_NOT_FOUND,
            )

    @extend_schema(
        request=RuternSerializer,
        responses={202: OpenApiResponse},
        description="return book for the user's library .",
    )
    @action(detail=False, methods=["post"])
    def return_book(self, request):
        username = request.data.get("username")
        book_id = request.data.get("book_id")
        if username and book_id:
            task = celery_return_book.delay(username, book_id)
            return Response({"task_id": task.id}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(
                {"error": "username and book_id is necassery"},
                status=status.HTTP_404_NOT_FOUND,
            )
