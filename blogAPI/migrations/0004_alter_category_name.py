# Generated by Django 4.2.17 on 2024-12-30 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogAPI', '0003_category_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
