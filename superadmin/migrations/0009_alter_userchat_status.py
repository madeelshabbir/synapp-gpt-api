# Generated by Django 4.2.1 on 2023-06-19 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("superadmin", "0008_alter_userchat_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userchat",
            name="status",
            field=models.IntegerField(default=0, null=True),
        ),
    ]
