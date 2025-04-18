from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.user import UserViewSet, CreateUserView
from .views.transfer import TransferViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="users")
router.register(r"transfers", TransferViewSet, basename="transactions")

urlpatterns = [
    path("", include(router.urls)),
    path("users/create", CreateUserView.as_view(), name="create-user"),
]
