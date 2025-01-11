# Generated by Django 5.1.4 on 2025-01-11 18:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0180_rename_project_visit_count_repo_repo_visit_count"),
    ]

    operations = [
        migrations.AddField(
            model_name="suggestion",
            name="organization",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="website.organization",
            ),
        ),
    ]
