# Generated by Django 2.0.7 on 2018-07-06 06:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Things',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=253, verbose_name='物品名称')),
                ('update_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('img', models.ImageField(upload_to='picture/', verbose_name='图片上传')),
                ('home', models.CharField(max_length=253, verbose_name='所属房间')),
                ('user', models.CharField(max_length=64, verbose_name='用户名')),
                ('desc', models.TextField(verbose_name='物品描述')),
                ('voice', models.FileField(upload_to='voice', verbose_name='音频上传')),
            ],
            options={
                'verbose_name': 'Thing',
                'db_table': 'Things',
            },
        ),
    ]