# Generated by Django 4.2.1 on 2023-06-08 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("superadmin", "0002_parameter"),
    ]

    operations = [
        migrations.CreateModel(
            name="Subcriber",
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
                ("subcriber", models.IntegerField()),
                ("unsubcriber", models.IntegerField()),
            ],
        ),
    ]
