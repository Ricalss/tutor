# Generated by Django 4.1 on 2024-05-08 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lessons", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="session_key",
            field=models.CharField(default=0, max_length=64),
            preserve_default=False,
        ),
    ]
