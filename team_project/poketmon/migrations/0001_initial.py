# Generated by Django 4.2.6 on 2023-11-10 13:06

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="monster",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                ("type", models.CharField(max_length=200)),
                ("classify", models.CharField(max_length=200)),
                ("gender", models.CharField(max_length=200)),
                ("description", models.CharField(max_length=200)),
                ("evolution", models.CharField(max_length=200)),
                ("img", models.URLField()),
            ],
        ),
    ]
