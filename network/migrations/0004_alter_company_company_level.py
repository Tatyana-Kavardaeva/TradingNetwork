# Generated by Django 5.1.4 on 2024-12-25 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_company_company_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='company_level',
            field=models.PositiveIntegerField(verbose_name='Уровень иерархии торговой компании'),
        ),
    ]
