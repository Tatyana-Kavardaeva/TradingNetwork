from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator

from network.models import Company
from network.validators import SupplierTypeValidator


class CompanySerializer(serializers.ModelSerializer):
    """ Serializer для модели Company. """

    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=Company.objects.all(), message="Такой email уже зарегистрирован.")]
    )

    class Meta:
        model = Company
        fields = '__all__'
        read_only_fields = ('company_level',)
        validators = [
            SupplierTypeValidator(['type', 'supplier']),
            UniqueTogetherValidator(queryset=Company.objects.all(), fields=['name', 'type', 'country', 'city'],
                                    message="Компания уже существует в этом регионе."),
        ]

    def update(self, instance, validated_data):
        """ Удаляет возможность обновлять поле 'задолженность перед поставщиком'. """

        validated_data.pop('debt', None)

        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance
