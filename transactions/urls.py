from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, CreateUserView

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('users/create', CreateUserView.as_view())
]
