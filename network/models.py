from django.db import models

NULLABLE = {"blank": True, "null": True}
COMPANY_TYPE = [
    ('factory', 'Завод'),
    ('retail', 'Розничная сеть'),
    ('individual', 'Индивидуальный предприниматель'),
]


class Company(models.Model):
    """ Модель торговой компании. """

    name = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(**NULLABLE, verbose_name='Описание')

    email = models.EmailField(verbose_name='email')
    country = models.CharField(max_length=100, verbose_name='Страна')
    city = models.CharField(max_length=100, verbose_name='Город')
    street = models.CharField(max_length=100, **NULLABLE, verbose_name='Улица')
    house_number = models.CharField(max_length=10, **NULLABLE, verbose_name='Номер дома')

    type = models.CharField(max_length=20, choices=COMPANY_TYPE, verbose_name='Тип компании')
    supplier = models.ForeignKey('self', on_delete=models.SET_NULL, **NULLABLE, related_name='suppliers',
                                 verbose_name='Поставщик')
    debt = models.DecimalField(max_digits=10, decimal_places=2, default=0.00,
                               verbose_name='Задолженность перед поставщиком')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Торговая компания'
        verbose_name_plural = 'Торговые компании'
        ordering = ['pk']


class Product(models.Model):
    """ Модель продукта. """
    name = models.CharField(max_length=255, verbose_name='Название')
    model = models.CharField(max_length=100, verbose_name='Модель')
    release_date = models.DateField(verbose_name='Дата выхода продукта на рынок')

    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='products',
                                verbose_name='Торговая компания')

    def __str__(self):
        return f"{self.name} ({self.model})"

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['pk']
