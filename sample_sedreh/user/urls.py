from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = "user"
router = DefaultRouter()
urlpatterns = []

router.register("user", views.ViewUserRegisteration, basename="user_stting")
router.register("library", views.LibraryView, basename="library")
router.register("otp", views.OtpCodeView, basename="otp_code")


urlpatterns += router.urls
