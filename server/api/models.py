import time

from django.contrib.auth.models import AbstractUser
from django.db import models

from common.base.daobase import AESCharField


class UserInfo(AbstractUser):
    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = "用户信息"


class DbBaseModel(models.Model):
    owner_id = models.ForeignKey(to='UserInfo', verbose_name="所属用户", on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    updated_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        abstract = True


class AliyunDrive(DbBaseModel):
    user_name = models.CharField(max_length=128, verbose_name="云盘用户名")
    nick_name = models.CharField(max_length=128, verbose_name="昵称")
    user_id = models.CharField(max_length=32, verbose_name="用户ID")
    default_drive_id = models.CharField(max_length=16, verbose_name="存储ID")
    default_sbox_drive_id = models.CharField(max_length=16, verbose_name="保险箱ID")
    access_token = AESCharField(max_length=1536, verbose_name="访问token")
    refresh_token = AESCharField(max_length=512, verbose_name="刷新token")
    avatar = models.CharField(max_length=512, verbose_name="头像地址")
    expire_time = models.DateTimeField(verbose_name="过期信息", auto_now_add=True)
    x_device_id = models.CharField(verbose_name="设备ID", max_length=128)

    used_size = models.BigIntegerField(verbose_name="已经使用空间", default=0)
    total_size = models.BigIntegerField(verbose_name="总空间大小", default=0)
    description = models.CharField(max_length=256, default='', verbose_name="备注信息", blank=True)
    enable = models.BooleanField(default=True, verbose_name="是否启用")
    active = models.BooleanField(default=True, verbose_name="密钥是否可用")

    class Meta:
        verbose_name = '阿里云网盘认证信息'
        verbose_name_plural = "阿里云网盘认证信息"
        unique_together = ('owner_id', 'user_id')

    def __str__(self):
        return f"所属用户:{self.owner_id}-网盘用户名:{self.user_name}-网盘昵称:{self.nick_name}-是否启用:{self.enable}"


class AliyunFileInfo(DbBaseModel):
    aliyun_drive_id = models.ForeignKey(to=AliyunDrive, on_delete=models.CASCADE, verbose_name="所属阿里云盘ID")

    name = models.CharField(max_length=256, verbose_name="文件名字")
    file_id = models.CharField(max_length=64, verbose_name="文件id")
    drive_id = models.CharField(max_length=64, verbose_name="drive_id")
    created_at = models.DateTimeField(verbose_name="上传时间", auto_now_add=True)
    size = models.BigIntegerField(verbose_name="文件大小")
    content_type = models.CharField(max_length=64, verbose_name="文件类型")
    category = models.CharField(max_length=64, verbose_name="类别")
    content_hash = models.CharField(max_length=64, verbose_name="content_hash")
    crc64_hash = models.CharField(max_length=64, verbose_name="crc64_hash")

    downloads = models.BigIntegerField(verbose_name="下载次数", default=0)

    class Meta:
        verbose_name = '文件信息'
        verbose_name_plural = "文件信息"

    def delete(self, using=None, keep_parents=False):
        if self.bookfileinfo:
            self.bookfileinfo.delete()
        super().delete(using, keep_parents)

    def __str__(self):
        return f"所属用户:{self.owner_id}-文件名:{self.name}-下载次数:{self.downloads}-文件大小:{self.size}"


class BookLabels(models.Model):
    name = models.CharField(max_length=32, verbose_name="标签名称")
    label_type_choices = ((1, '书籍标签'), (2, '书籍类别'), (3, '书籍评价'))
    label_type = models.SmallIntegerField(choices=label_type_choices, default=0, verbose_name="标签类型")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    updated_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = '书籍标签'
        verbose_name_plural = "书籍标签"
        unique_together = (('name', 'label_type'),)

    @staticmethod
    def get_tags():
        return BookLabels.objects.filter(label_type=1)

    @staticmethod
    def get_categories():
        return BookLabels.objects.filter(label_type=2)

    @staticmethod
    def get_grading():
        return BookLabels.objects.filter(label_type=3)

    def __str__(self):
        return f"书籍标签:{self.name}-类型:{self.get_label_type_display()}"


def default_grading():
    return []


def book_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    prefix = filename.split('.')[-1]
    new_filename = str(time.time()).replace('.', '')
    return time.strftime(f"{instance.owner_id.id}/%Y/%m/%d/%S/{new_filename}.{prefix}")


class BookFileInfo(DbBaseModel):
    file = models.OneToOneField(to=AliyunFileInfo, on_delete=models.CASCADE, verbose_name="存储信息")
    name = models.CharField(max_length=256, verbose_name="书籍名称")
    introduction = models.CharField(max_length=2048, verbose_name="书籍简介", null=True, blank=True)
    cover = models.FileField(verbose_name="书籍封面", null=True, blank=True, upload_to=book_directory_path)
    author = models.CharField(max_length=32, verbose_name="书籍作者")
    downloads = models.BigIntegerField(verbose_name="下载次数", default=0)
    size = models.BigIntegerField(verbose_name="文件大小")
    grading = models.JSONField(verbose_name="书籍评分", default=default_grading)
    tags = models.ManyToManyField(verbose_name="书籍标签", to=BookLabels, related_name='tags', null=True, blank=True)
    categories = models.ForeignKey(verbose_name="书籍类别", to=BookLabels, on_delete=models.SET_NULL, null=True,
                                   blank=True, related_name='categories')
    publish = models.BooleanField(verbose_name="是否发布", default=True)

    class Meta:
        verbose_name = '书籍信息'
        verbose_name_plural = "书籍信息"

    def delete(self, using=None, keep_parents=False):
        if self.cover:
            self.cover.delete()
        super().delete(using, keep_parents)

    def __str__(self):
        return f"所属用户:{self.owner_id}-文件名:{self.name}-下载次数:{self.downloads}"
