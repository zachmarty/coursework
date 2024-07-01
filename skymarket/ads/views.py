from rest_framework import viewsets
from rest_framework.response import Response
from ads.models import Ad, Comment
from ads.paginators import AdPaginator, CommentPaginator
from ads.serializers import AdDetailSerializer, AdSerializer, CommentSerializer
from rest_framework.generics import ListAPIView
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from ads.permissions import IsAuthorOrSuper
from users.models import User


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
    serializer_class = CommentSerializer
    queryset = Ad.objects.all()
    pagination_class = CommentPaginator

    def get_permissions(self):
        if self.action in ["partial_update", "destroy"]:
            self.permission_classes = [IsAuthenticated, IsAuthorOrSuper]
        return [permission() for permission in self.permission_classes]

    def get_queryset(self):
        ad = self.kwargs["ad_id"]
        ad = Ad.objects.filter(id=ad)
        if not ad.exists():
            raise NotFound
        ad = ad.first()
        queryset = Comment.objects.filter(ad=ad)
        return self.paginate_queryset(queryset)

    def paginate_queryset(self, queryset):
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        output_data = []
        for comment in serializer.data:
            obj = Comment.objects.get(id = comment['id'])
            tmp = {
                "pk": comment["id"],
                "text": comment["text"],
                "author_id": obj.author.id,
                "created_at": comment["created_at"],
                "author_first_name": obj.author.first_name,
                "author_last_name": obj.author.last_name,
                "ad_id": obj.ad.id,
                "author_image": obj.author.image,
            }
            output_data.append(tmp)
        return self.get_paginated_response(output_data)

    def create(self, request, *args, **kwargs):
        data = request.data
        user = self.request.user
        instance = self.get_serializer(data=data)
        instance.is_valid(raise_exception=True)
        ad = self.kwargs["ad_id"]
        ad = Ad.objects.filter(id=ad).first()
        new_comment = Comment.objects.create(text=data["text"], author=user, ad=ad)
        new_comment.save()
        output_data = {
            "pk": new_comment.id,
            "text": new_comment.text,
            "author_id": user.id,
            "created_at": new_comment.created_at,
            "author_first_name": user.first_name,
            "author_last_name": user.last_name,
            "ad_id": ad.id,
            "author_image": user.image,
        }
        return Response(output_data)

    def retrieve(self, request, *args, **kwargs):
        ad = self.kwargs["ad_id"]
        ad = Ad.objects.filter(id=ad)
        if not ad.exists():
            raise NotFound
        ad = ad.first()
        comment = Comment.objects.filter(id=kwargs["pk"])
        if not comment.exists():
            raise NotFound
        comment = comment.first()
        if not comment.ad == ad:
            raise NotFound
        user = self.request.user
        output_data = {
            "pk": comment.id,
            "text": comment.text,
            "author_id": user.id,
            "created_at": comment.created_at,
            "author_first_name": user.first_name,
            "author_last_name": user.last_name,
            "ad_id": ad.id,
            "author_image": user.image,
        }
        return Response(output_data)

    def update(self, request, *args, **kwargs):
        comment = Comment.objects.filter(id=kwargs["pk"])
        if not comment.exists():
            raise NotFound
        comment = comment.first()
        ad = Ad.objects.filter(id=kwargs["ad_id"])
        if not ad.exists():
            raise NotFound
        ad = ad.first()
        if not comment.ad == ad:
            raise NotFound
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        comment.text = data["text"]
        comment.save()
        user = self.request.user
        output_data = {
            "pk": comment.id,
            "text": comment.text,
            "author_id": user.id,
            "created_at": comment.created_at,
            "author_first_name": user.first_name,
            "author_last_name": user.last_name,
            "ad_id": ad.id,
            "author_image": user.image,
        }
        return Response(output_data)

    def destroy(self, request, *args, **kwargs):
        comment = Comment.objects.filter(id=kwargs["pk"])
        if not comment.exists():
            raise NotFound
        comment = comment.first()
        ad = Ad.objects.filter(id=kwargs["ad_id"])
        if not ad.exists():
            raise NotFound
        ad = ad.first()
        if not comment.ad == ad:
            raise NotFound
        comment.delete()
        return Response({"detail": "success"})
