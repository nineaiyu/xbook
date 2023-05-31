# Generated by Django 4.2.1 on 2023-05-24 03:20

import django.contrib.auth.models
import django.contrib.auth.validators
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models

import api.models
import common.base.daobase


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': '用户信息',
                'verbose_name_plural': '用户信息',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='AliyunDrive',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('user_name', models.CharField(max_length=128, verbose_name='云盘用户名')),
                ('nick_name', models.CharField(max_length=128, verbose_name='昵称')),
                ('user_id', models.CharField(max_length=32, verbose_name='用户ID')),
                ('default_drive_id', models.CharField(max_length=16, verbose_name='存储ID')),
                ('default_sbox_drive_id', models.CharField(max_length=16, verbose_name='保险箱ID')),
                ('access_token', common.base.daobase.AESCharField(max_length=1536, verbose_name='访问token')),
                ('refresh_token', common.base.daobase.AESCharField(max_length=512, verbose_name='刷新token')),
                ('avatar', models.CharField(max_length=512, verbose_name='头像地址')),
                ('expire_time', models.DateTimeField(auto_now_add=True, verbose_name='过期信息')),
                ('x_device_id', models.CharField(max_length=128, verbose_name='设备ID')),
                ('used_size', models.BigIntegerField(default=0, verbose_name='已经使用空间')),
                ('total_size', models.BigIntegerField(default=0, verbose_name='总空间大小')),
                ('description', models.CharField(blank=True, default='', max_length=256, verbose_name='备注信息')),
                ('enable', models.BooleanField(default=True, verbose_name='是否启用')),
                ('active', models.BooleanField(default=True, verbose_name='密钥是否可用')),
                ('owner_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='所属用户')),
            ],
            options={
                'verbose_name': '阿里云网盘认证信息',
                'verbose_name_plural': '阿里云网盘认证信息',
                'unique_together': {('owner_id', 'user_id')},
            },
        ),
        migrations.CreateModel(
            name='AliyunFileInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(max_length=256, verbose_name='文件名字')),
                ('file_id', models.CharField(max_length=64, verbose_name='文件id')),
                ('drive_id', models.CharField(max_length=64, verbose_name='drive_id')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='上传时间')),
                ('size', models.BigIntegerField(verbose_name='文件大小')),
                ('content_type', models.CharField(max_length=64, verbose_name='文件类型')),
                ('category', models.CharField(max_length=64, verbose_name='类别')),
                ('content_hash', models.CharField(max_length=64, verbose_name='content_hash')),
                ('crc64_hash', models.CharField(max_length=64, verbose_name='crc64_hash')),
                ('downloads', models.BigIntegerField(default=0, verbose_name='下载次数')),
                ('aliyun_drive_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.aliyundrive', verbose_name='所属阿里云盘ID')),
                ('owner_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='所属用户')),
            ],
            options={
                'verbose_name': '文件信息',
                'verbose_name_plural': '文件信息',
            },
        ),
        migrations.CreateModel(
            name='BookLabels',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='标签名称')),
                ('label_type', models.SmallIntegerField(choices=[(1, '书籍标签'), (2, '书籍类别'), (3, '书籍评价')], default=0, verbose_name='标签类型')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '书籍标签',
                'verbose_name_plural': '书籍标签',
                'unique_together': {('name', 'label_type')},
            },
        ),
        migrations.CreateModel(
            name='BookFileInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(max_length=256, verbose_name='书籍名称')),
                ('introduction', models.CharField(blank=True, max_length=2048, null=True, verbose_name='书籍简介')),
                ('cover', models.FileField(blank=True, null=True, upload_to=api.models.book_directory_path,
                                           verbose_name='书籍封面')),
                ('author', models.CharField(max_length=32, verbose_name='书籍作者')),
                ('downloads', models.BigIntegerField(default=0, verbose_name='下载次数')),
                ('size', models.BigIntegerField(verbose_name='文件大小')),
                ('grading', models.JSONField(default=api.models.default_grading, verbose_name='书籍评分')),
                ('publish', models.BooleanField(default=True, verbose_name='是否发布')),
                ('categories', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                                 related_name='categories', to='api.booklabels',
                                                 verbose_name='书籍类别')),
                ('file', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.aliyunfileinfo',
                                              verbose_name='存储信息')),
                ('owner_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL,
                                               verbose_name='所属用户')),
                ('tags', models.ManyToManyField(blank=True, null=True, related_name='tags', to='api.booklabels',
                                                verbose_name='书籍标签')),
            ],
            options={
                'verbose_name': '书籍信息',
                'verbose_name_plural': '书籍信息',
            },
        ),
    ]
