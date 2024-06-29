from rest_framework import viewsets
from rest_framework.response import Response
from ads.models import Ad
from ads.paginators import AdPaginator
from ads.serializers import AdDetailSerializer, AdSerializer
from rest_framework.generics import ListAPIView
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from ads.permissions import IsAuthorOrSuper


# TODO view функции. Предлагаем Вам следующую структуру - но Вы всегда можете использовать свою
class AdViewSet(viewsets.ModelViewSet):
    serializer_class = AdSerializer
    queryset = Ad.objects.all()
    pagination_class = AdPaginator

    def get_serializer_class(self):
        if self.action in ["create", "retrieve", "partial_update"]:
            return AdDetailSerializer
        return AdSerializer
    
    def get_permissions(self):
        if self.action in ["partial_update", "destroy"]:
            self.permission_classes = [IsAuthenticated, IsAuthorOrSuper]
        return [permission() for permission in self.permission_classes]

    def create(self, request, *args, **kwargs):
        data = request.data
        user = self.request.user
        data["author_id"] = user.id
        data["phone"] = str(user.phone)
        data["author_first_name"] = user.first_name
        data["author_last_name"] = user.last_name
        instance = self.get_serializer(data=data)
        instance.is_valid(raise_exception=True)
        data["image"] = instance.validated_data.get("image")
        data["description"] = instance.validated_data.get("description")
        data["author"] = user
        new_ad = Ad.objects.create(
            title=data["title"],
            author=data["author"],
            price=data["price"],
            image=data["image"],
            description=data["description"],
        )
        new_ad.save()
        return Response(instance.data)

    def retrieve(self, request, *args, **kwargs):
        instance = Ad.objects.filter(id=kwargs["pk"])
        if instance.exists():
            instance = instance.first()
            data = {}
            user = self.request.user
            data["title"] = instance.title
            data["price"] = instance.price
            data["description"] = instance.description
            data["image"] = instance.image
            data["phone"] = str(user.phone)
            data["author_id"] = user.id
            data["author_first_name"] = user.first_name
            data["author_last_name"] = user.last_name
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.validated_data)
        else:
            raise NotFound

    def update(self, request, *args, **kwargs):
        instance = Ad.objects.filter(id=kwargs["pk"])
        if not instance.exists():
            raise NotFound
        instance = instance.first()
        print(self.get_serializer_class())
        data = request.data
        user = self.request.user
        data["phone"] = str(user.phone)
        data["author_id"] = user.id
        data["author_first_name"] = user.first_name
        data["author_last_name"] = user.last_name
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        instance.title = serializer.validated_data.get("title")
        instance.description = serializer.validated_data.get("description")
        instance.price = serializer.validated_data.get("price")
        instance.image = serializer.validated_data.get("image")
        data["image"] = serializer.validated_data.get("image")
        data["description"] = serializer.validated_data.get("description")
        instance.save()
        return Response(data)


class MyAdsView(ListAPIView):
    serializer_class = AdSerializer
    queryset = Ad.objects.all()
    pagination_class = AdPaginator

    def get_queryset(self):
        queryset = Ad.objects.filter(author=self.request.user)
        return queryset


class CommentViewSet(viewsets.ModelViewSet):
    pass
