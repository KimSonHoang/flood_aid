# Generated by Django 4.2.16 on 2024-10-27 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("donations", "0004_donation"),
    ]

    operations = [
        migrations.AlterField(
            model_name="donation",
            name="transaction_id",
            field=models.CharField(blank=True, default="", max_length=100),
            preserve_default=False,
        ),
    ]
