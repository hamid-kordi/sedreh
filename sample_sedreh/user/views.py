from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, ModelViewSet
from .models import User, OtpCode, Library
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter
from rest_framework import status
from .serializers import (
    UserEditSerializer,
    UserRegisterSerializer,
    OtpCodeSerializer,
    LibrarySerializer,
    IncreaseBudgetSerializer,
    BuyBookSerializer,
    RuternSerializer,
    UserShowDtat,
)
from celery.result import AsyncResult
from .tasks import celery_buy_book, celery_increaseـtheـbudget, celery_return_book
from rest_framework.views import APIView


class ViewUserRegisteration(ViewSet):
    query_set = User.objects.all()

    authentication_classes = [JWTAuthentication]
    # permission_classes = (IsAuthenticated, IsUser)

    def retrieve(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
            ser_data = UserRegisterSerializer(user)
            return Response(ser_data.data)
        except User.DoesNotExist:
            return Response(
                data={"error": "user does not exist"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
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
            ser_data.create()
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
    authentication_classes = [JWTAuthentication]
    queryset = Library.objects.all()
    serializer_class = LibrarySerializer


class OtpCodeView(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    queryset = OtpCode.objects.all()
    serializer_class = OtpCodeSerializer


class BudgetManage(ViewSet):
    authentication_classes = [JWTAuthentication]
    """
    To increase the amount of the wallet and also to return the book
    and also to buy the book

    """

    @extend_schema(
        responses={202: OpenApiResponse},
        description="Increase the user's budget using OTP code.",
    )
    @action(detail=False, methods=["post"])
    def increaseـtheـbudget(self, request):
        username = request.data.get("username")
        user = User.objects.filter(username=username).first()
        code = request.data.get("code")
        if (user is not None) and code:
            user_id = user.id
            task = celery_increaseـtheـbudget.delay(user_id, code)
            return Response({"task_id": task.id}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(
                {"error": "user or code not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

    @extend_schema(
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

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="task_id",
                description="task result",
                required=True,
                type=str,
            )
        ],
        description="Get user data",
    )
    @action(detail=False, methods=["get"])
    def get_task_detail(self, request):
        task_id = request.query_params.get("task_id")
        if not task_id:
            return Response({"error": "task_id is required"}, status=400)
        result = AsyncResult(id=task_id)
        if result.state == "PENDING":
            return Response({"status": "Pending"}, status=202)
        elif result.state == "SUCCESS":
            return Response(result.result, status=200)
        elif result.state == "STARTED":
            return Response({"status": "Started"}, status=202)
        else:
            return Response(
                {"status": result.state, "message": str(result.info)}, status=400
            )
