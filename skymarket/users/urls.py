from django.urls import include, path
from users.views import UsersViewSet
from users.apps import UsersConfig
from rest_framework.routers import DefaultRouter

# TODO подключите UserViewSet из Djoser.views к нашим urls.py
# TODO для этокого рекоммендуется использовать SimpleRouter

app_name = UsersConfig.name
router = DefaultRouter()
router.register(r"users", UsersViewSet, basename="users")


urlpatterns = [
    path("", include(router.urls), name="users"),
    path("", include("djoser.urls.authtoken")),
]
