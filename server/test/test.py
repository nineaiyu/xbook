#!/usr/bin/env python
# -*- coding:utf-8 -*-
# project : server
# filename : test
# author : ly_13
# date : 5/24/2023
import json
import os
import random
import time

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'xbook.settings')
django.setup()
from django.conf import settings
from api.views.upload import save_file_info
from api.models import AliyunDrive
from api.utils.drive import get_aliyun_drive

drive_obj = AliyunDrive.objects.first()


def upload_local_file(file_path):
    ali_obj = get_aliyun_drive(drive_obj)
    file_name = os.path.basename(file_path)
    remote_file_path = f'{settings.XBOOKSTORE}/{time.strftime(f"{drive_obj.owner_id_id}/%Y/%m/%d/{file_name}")}'
    complete = ali_obj.local_upload_file(file_path=file_path, name=remote_file_path)
    if getattr(complete, 'rapid_upload'):
        complete = ali_obj.get_file(complete.file_id, complete.drive_id)
    return save_file_info(complete, drive_obj.owner_id, drive_obj)


def updata():
    base_name = os.path.dirname(os.path.dirname(__file__))
    zxcs_dir = os.path.join(base_name, 'tools', 'zxcs')
    for file_name in os.listdir(zxcs_dir):
        if file_name.endswith('.rar'):
            file_path = os.path.join(base_name, 'tools', 'zxcs', file_name)
            ok_path = os.path.join(base_name, 'tools', 'zxcs_ok', file_name)
            upload_local_file(file_path)
            os.rename(file_path, ok_path)


from api.models import BookTemp, AliyunFileInfo, BookFileInfo, BookLabels

# ranklist = pd.read_excel('ranklist.xls')
# z=0
# for i in range(len(ranklist)):
#     book_info = ranklist.iloc[i]
#     name = book_info['Title']
#     author = book_info['Author']
#     flower = f"{book_info['XianCao']},{book_info['LiangCao']},{book_info['GanCao']},{book_info['KuCao']},{book_info['DuCao']}"
#     x=BookTemp.objects.filter(name__icontains=f"《{name}》").filter(name__icontains=author).all()
#     if x.count() == 1:
#         if x.first().book_name:
#             continue
#         print(name)
#         x.update(flowers=flower, author=author,book_name=name)
#     if x.count()==0:
#         z+=1
#         BookTemp.objects.create(flowers=flower, author=author,book_name=name, is_new=True)
#         print('新增书籍',z, name, author, flower)



bt_list = BookTemp.objects.filter(downloadurl=1).all()
# print(bt_list.count())
# exit()
tags_list = list(BookLabels.get_tags().all())

for b in bt_list:
    ali_file_obj = AliyunFileInfo.objects.filter(name__icontains=b.book_name.replace('【断更】','').split(' ')[0]).filter(name__icontains=b.author.replace('【断更】','').split(' ')[0]).all()
    if ali_file_obj.count() == 1:
        b_type = b.types

        if b_type and len(b_type) == 4:
            x = random.choice([0, 1])
            b_type = b_type[x * 2:2 + x * 2]
        if b_type :
            categories = BookLabels.get_categories().filter(name__icontains=b_type).first()
        else:
            categories = random.choice(BookLabels.get_categories().all())

        nn = BookFileInfo.objects.filter(file=ali_file_obj.first()).first()
        if nn:
            # nn.created_time = b.create_time
            # nn.updated_time = b.create_time
            # nn.save(update_fields=['created_time', 'updated_time'])
            continue
        print(b.name, categories, ali_file_obj)

        nn = BookFileInfo.objects.create(file=ali_file_obj.first(), name=b.name.split('作者')[0],
                                         introduction=b.description.replace('\u3000', ''),
                                         author=b.author, size=b.size,
                                         # grading=json.loads(f'[{b.flowers}]'),
                                         categories=categories,
                                         created_time=b.create_time,
                                         updated_time=b.create_time,
                                         owner_id_id=1
                                         )
        nn.tags.set(random.sample(tags_list, random.randint(3, 15)))
        nn.created_time=b.create_time
        nn.updated_time=b.create_time
        nn.save(update_fields=['created_time','updated_time'])
    if ali_file_obj.count() > 1:
        print(ali_file_obj.count(),f"{b.book_name},{b.author}",ali_file_obj)
    if ali_file_obj.count() == 0:
        print(0,b.book_name,b.author, ali_file_obj)

exit()
#
#
# book = BookFileInfo.objects.first()
#
# b_c = BookLabels.get_grading().count()
# for label, grade in zip(range(b_c), book.grading + [0] * (b_c - len(book.grading))):
#     print(label, grade)

n = {'page': ['1'], 'size': ['10'], 'categories': ['[301,303,299]'], 'search': [''],
     'ordering': ['-created_time']}
result = {}
for key in sorted(n):
    result.setdefault(key, n.get(key)[0])
print(result)
print(json.dumps(result))

x = collections.OrderedDict(sorted(n.items(), key=lambda s: s[0]))
print(x)
print(json.dumps(x))
print(11111111111)
print(json.dumps(sorted(n.items(), key=lambda s: s[0])))
print()

print(base64.b64encode(md5(json.dumps(n, sort_keys=True).encode('utf-8')).digest()).decode('utf-8'))


def sorted_query(n, y={}):
    for key in sorted(n):
        try:
            x = json.loads(n.get(key))
            y.setdefault(key, sorted_query(x, y))
        except:
            y.setdefault(key, n.get(key))
    return y


# print(sorted_query({'x':'[4,6,2]'}))
exit()

x = BookFileInfo.objects.filter(file__id='30').first()
print(x)
exit()
x = datetime.datetime.now() - datetime.timedelta(days=1)
print(x)
z = queryset = BookFileInfo.objects.filter(publish=True, ).filter(created_time__gt=x).values('created_time').order_by(
    '-created_time')
print(z)
