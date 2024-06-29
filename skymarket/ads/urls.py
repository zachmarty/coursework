from django.urls import include, path
from rest_framework.routers import DefaultRouter
from ads.views import AdViewSet, CommentViewSet, MyAdsView
from ads.apps import SalesConfig

# TODO настройка роутов для модели

app_name = SalesConfig.name

router_ads = DefaultRouter()
router_comments = DefaultRouter()
router_ads.register(r"ads", AdViewSet, basename="ads")
router_comments.register(r"comments", CommentViewSet, basename="comments")
urlpatterns = [
    path("ads/me", MyAdsView.as_view(), name="my_ads_list"),
    path("ads/<int:ad_id>/", include(router_comments.urls), name="comments"),
] + router_ads.urls
