from rest_framework import serializers


class SupplierTypeValidator:
    """ Проверяет правила заполнения полей 'поставщик' и 'тип компании'. """

    def __init__(self, fields):
        self.fields = fields

    def __call__(self, data):
        supplier = data.get('supplier')
        company_type = data.get('type')

        if company_type is None:
            raise serializers.ValidationError("Укажите тип компании.")

        # Проверяет наличие поставщика у розницы и ИП
        if supplier is None and company_type in ['retail', 'individual']:
            raise serializers.ValidationError("Выберите поставщика.")

        # Проверяет, чтобы завод не имел поставщика
        if supplier and company_type == 'factory':
            raise serializers.ValidationError("Завод не может иметь поставщика.")

        # Проверяет типы поставщика
        if supplier and company_type == 'retail' and supplier.type == 'individual':
            raise serializers.ValidationError("ИП не может быть поставщиком для розницы.")

        # Проверяет уровни иерархии
        if supplier and supplier.company_level == 2:
            raise serializers.ValidationError("Компания с уровнем 2 не может быть поставщиком.")
