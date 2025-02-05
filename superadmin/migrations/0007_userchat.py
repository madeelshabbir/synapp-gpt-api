# Generated by Django 4.2.1 on 2023-06-19 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("superadmin", "0006_statistic_alter_countunsubcriber_created_at"),
    ]

    operations = [
        migrations.CreateModel(
            name="Userchat",
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
                ("user_info", models.CharField(max_length=100)),
                ("question", models.TextField()),
                ("answer", models.TextField()),
                ("created_at", models.DateField()),
                ("status", models.BooleanField(default=False)),
            ],
        ),
    ]
