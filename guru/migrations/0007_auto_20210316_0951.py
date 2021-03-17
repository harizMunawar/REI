# Generated by Django 3.0.5 on 2021-03-16 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guru', '0006_auto_20210310_1643'),
    ]

    operations = [
        migrations.AddField(
            model_name='guru',
            name='first_login',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='guru',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last login'),
        ),
    ]