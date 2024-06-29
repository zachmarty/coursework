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
    phone = serializers.CharField()
    author_first_name = serializers.CharField()
    author_last_name = serializers.CharField()
    author_id = serializers.IntegerField()

    class Meta:
        model = Ad
        fields = [
            "title",
            "price",
            "description",
            "image",
            "phone",
            "author_first_name",
            "author_last_name",
            "author_id",
        ]
