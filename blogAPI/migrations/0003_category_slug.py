# Generated by Django 4.2.17 on 2024-12-30 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogAPI', '0002_category_language'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, max_length=60, unique=True),
        ),
    ]
