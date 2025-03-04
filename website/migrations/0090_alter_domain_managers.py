# Generated by Django 5.0.2 on 2024-04-20 23:10

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0089_merge_20240321_2353"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="domain",
            name="managers",
            field=models.ManyToManyField(blank=True, related_name="user_domains", to=settings.AUTH_USER_MODEL),
        ),
    ]
