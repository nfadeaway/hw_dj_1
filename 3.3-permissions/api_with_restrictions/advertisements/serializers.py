from django.contrib.auth.models import User
from rest_framework import serializers

from advertisements.models import Advertisement, Fav


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at')

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""
        adv_status_open = Advertisement.objects.filter(creator=self.context["request"].user.pk).filter(
            status="OPEN").count()
        if adv_status_open >= 10:
            if self.context["view"].action == "create":
                raise serializers.ValidationError('У вас уже 10 открытых объявлений! Вы не можете создать новое!')
            if self.context["view"].action == "partial_update" and data["status"] == "OPEN":
                raise serializers.ValidationError('У вас уже 10 открытых объявлений! Вы не можете открыть больше!')

        return data


class FavSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fav
        fields = ['advertisement_id', 'is_fav']


class ShowFavSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    favorites = FavSerializer(many=True)

    class Meta:
        model = Advertisement
        fields = ['user', 'favorites']
