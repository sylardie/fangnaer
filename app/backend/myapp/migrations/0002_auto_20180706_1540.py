# Generated by Django 2.0.7 on 2018-07-06 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='things',
            name='update_time',
            field=models.DateTimeField(default='2018-07-06 15:07:00', verbose_name='添加时间'),
        ),
    ]
