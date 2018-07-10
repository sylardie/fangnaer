from datetime import datetime
from django.db import models

# Create your models here.


class Things(models.Model):
    name = models.CharField(max_length=253, verbose_name='物品名称')
    update_time = models.DateTimeField(default=datetime.now().strftime('%Y-%m-%d %H:%m:%S'), verbose_name='添加时间')
    img = models.ImageField(blank=True, null=True, upload_to='picture/', verbose_name='图片上传')
    home = models.CharField(max_length=253, verbose_name='所属房间')
    user = models.CharField(max_length=64, verbose_name='用户名')
    desc = models.TextField(blank=True, null=True, verbose_name='物品描述')
    voice = models.FileField(blank=True, null=True, upload_to='voice', verbose_name='音频上传')

    class Meta:
        # 指明一个易于理解和表示的单词形式的对象
        verbose_name = 'Thing'
        # 声明数据表的名
        db_table = 'Things'

    def __str__(self):
        return self.name


