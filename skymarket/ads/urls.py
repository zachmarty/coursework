from django.urls import include, path
from rest_framework.routers import DefaultRouter
from ads.views import AdViewSet, CommentViewSet
from ads.apps import SalesConfig
# TODO настройка роутов для модели

app_name = SalesConfig.name

router = DefaultRouter()
router.register(r"ads", AdViewSet, basename="ads")
router.register(r"comments", CommentViewSet, basename="comments")
urlpatterns = [

]+ router.urls
