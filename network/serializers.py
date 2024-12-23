from rest_framework import serializers
from network.models import Company, Product


class CompanySerializer(serializers.ModelSerializer):
    """ Serializer для модели Company. """

    company_level = serializers.SerializerMethodField(read_only=True)

    def get_company_level(self, instance):
        """ Получает уровень иерархии торговой компании. """

        if instance.supplier is None:
            return 0  # Завод
        elif instance.supplier.level == 0:
            return 1  # Компания, которая напрямую относится к заводу
        else:
            return 2  # Индивидуальный предприниматель или другие типы компаний

    class Meta:
        model = Company
        fields = '__all__'
        read_only_fields = ('debt',)
        # validators = [
        #     TitleValidator('title'),
        #     serializers.UniqueTogetherValidator(fields=["title"], queryset=Course.objects.all())
        # ]


class ProductSerializer(serializers.ModelSerializer):
    """ Serializer для модели Product. """

    class Meta:
        model = Product
        fields = '__all__'
