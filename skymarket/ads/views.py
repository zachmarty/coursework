from rest_framework import viewsets
from rest_framework.response import Response
from ads.models import Ad
from ads.paginators import AdPaginator
from ads.serializers import AdSerializer


# TODO view функции. Предлагаем Вам следующую структуру - но Вы всегда можете использовать свою
class AdViewSet(viewsets.ModelViewSet):
    serializer_class = AdSerializer
    queryset = Ad.objects.all()
    pagination_class = AdPaginator

    def create(self, request, *args, **kwargs):
        data = request.data
        user = self.request.user
        new_ad = Ad.objects.create(**data, author=user)
        new_ad.save()
        instance = AdSerializer(new_ad)
        instance.set_value(
            {
                "phone": user.phone,
                "author_first_name": user.first_name,
                "author_last_name": user.last_name,
                "author_id": user.id,
            }
        )
        return Response(instance.data)


class CommentViewSet(viewsets.ModelViewSet):
    pass
