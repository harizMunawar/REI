# Generated by Django 3.1.4 on 2020-12-15 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guru', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='guru',
            name='gender',
            field=models.CharField(choices=[('P', 'Pria'), ('W', 'Wanita')], default='P', max_length=1, verbose_name='Jenis Kelamin'),
        ),
    ]