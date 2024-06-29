from django.urls import include, path
from rest_framework.routers import DefaultRouter
from ads.views import AdViewSet, CommentViewSet, MyAdsView
from ads.apps import SalesConfig
# TODO настройка роутов для модели

app_name = SalesConfig.name

router = DefaultRouter()
router.register(r"ads", AdViewSet, basename="ads")
router.register(r"comments", CommentViewSet, basename="comments")
urlpatterns = [
    path("ads/me", MyAdsView.as_view(), name="my_ads_list")
]+ router.urls
