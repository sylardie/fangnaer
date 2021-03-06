# Generated by Django 2.0.7 on 2018-07-07 03:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_auto_20180706_1540'),
    ]

    operations = [
        migrations.AlterField(
            model_name='things',
            name='desc',
            field=models.TextField(blank=True, null=True, verbose_name='物品描述'),
        ),
        migrations.AlterField(
            model_name='things',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='picture/', verbose_name='图片上传'),
        ),
        migrations.AlterField(
            model_name='things',
            name='update_time',
            field=models.DateTimeField(default='2018-07-07 11:07:17', verbose_name='添加时间'),
        ),
        migrations.AlterField(
            model_name='things',
            name='voice',
            field=models.FileField(blank=True, null=True, upload_to='voice', verbose_name='音频上传'),
        ),
    ]
