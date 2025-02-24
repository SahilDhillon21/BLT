# Generated by Django 5.1.4 on 2025-01-04 19:10

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("comments", "0006_comment_author_fk"),
        ("contenttypes", "0002_remove_content_type_name"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="comment",
            name="issue",
        ),
        migrations.AddField(
            model_name="comment",
            name="content_type",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="contenttypes.contenttype",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="comment",
            name="object_id",
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
