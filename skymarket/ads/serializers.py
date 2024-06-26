from rest_framework import serializers

from ads.models import Ad
from ads.validators import PriceValidator


# TODO Сериалайзеры. Предлагаем Вам такую структуру, однако вы вправе использовать свою


class CommentSerializer(serializers.ModelSerializer):
    # TODO сериалайзер для модели
    pass


class AdSerializer(serializers.ModelSerializer):
    # TODO сериалайзер для модели
    class Meta:
        model = Ad
        fields = "__all__"
        validators = [PriceValidator(field="price")]


class AdDetailSerializer(serializers.ModelSerializer):
    # TODO сериалайзер для модели
    class Meta:
        model = Ad
        exclude = [
            "created_at",
        ]
        extra_kwargs = {
            "phone":{"required":True},
            "author_first_name":{"required":True},
            "author_last_name":{"required":True},
            "phone":{"required":True},
            "author_id":{"required":True},
        }
