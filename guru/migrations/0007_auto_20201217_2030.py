# Generated by Django 3.1.4 on 2020-12-17 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guru', '0006_guru_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guru',
            name='nama',
            field=models.CharField(max_length=255),
        ),
    ]
