from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from advertisements.models import Advertisement, AdvertisementStatusChoices


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(read_only=True)

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', )


    def create(self, validated_data):
        """Метод для создания"""

        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)


    def update(self, instance, validated_data):
        if instance.creator != self.context['request'].user:
            raise serializers.ValidationError("Вы не можете изменять чужие объявления")
        return super().update(instance, validated_data)

    # def delete(self, instance, validated_data):
    #     if instance.creator != self.context['request'].user:
    #         raise serializers.ValidationError("Вы не можете удалять чужие объявления")
    #     return super().update(instance, validated_data)


    def validate(self, data):
        # Проверка количества открытых объявлений у пользователя
        if self.instance is None:  # Только для создания
            user = self.context['request'].user
            open_ads_count = Advertisement.objects.filter(
                creator=user,
                status=AdvertisementStatusChoices.OPEN
            ).count()
            if open_ads_count >= 10:
                raise ValidationError("Превышено максимальное количество открытых объявлений (10)")
        return data
