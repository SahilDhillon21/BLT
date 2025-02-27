# Generated by Django 5.1.4 on 2025-02-27 21:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0210_lecture_description_section_description_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="lecturestatus",
            name="lecture",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name="lecture_statuses", to="website.lecture"
            ),
        ),
    ]
