#!/usr/bin/env python
# -*- coding:utf-8 -*-
# project : server
# filename : upload_cli
# author : ly_13
# date : 5/29/2023
import datetime
import os
import django
from pip._vendor import chardet

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'xbook.settings')
django.setup()
import re
import ftfy
from django.utils import timezone

x={}
count = 0
def read_file(d, file_path):
    global count
    with rarfile.RarFile(os.path.join(d,file_path)) as rf:
        for f in rf.infolist():
            head=[]
            dddd = [f.filename, f.file_size, f.date_time]
            if f.filename.lower().endswith('.txt'):
                with rf.open(f.filename) as f:
                    blist = f.readlines(1500)
                    context = b"".join(blist)
                    z=chardet.detect(context)
                    coding = z['encoding']
                    if x.get(coding):
                        x[coding]+=1
                    else:
                        x[coding] = 1

                count=count+1
                if count%100==0:
                    print(count, x)

                h=''
                # head.append(coding)
                for i in range(len(blist)):
                    c = blist[i]
                    # if i in [0, 1, 2, 5]:
                    #     continue
                    try:
                        text = c.decode(coding).replace('\u3000\u3000','')
                        head.append(text.replace('\r\n', ''))
                        if re.search('^[第|一|1|序|自序|楔子|前奏]', text) and h == '\r\n':
                            head.pop()
                            break
                        h = text
                    except Exception as e:
                        pass
                        # print(c,e)
                print( dddd, "".join(head).replace('\u3000',''))
                return dddd, "".join(head).split('内容简介')[1].replace('\u3000','')

                # try:
                #     text = context.decode(coding)
                #     print(head, text)
                # except Exception as e:
                #     print(head, e,context)


                # with rf.open(f.filename) as f:
                #     h=''
                #     for i in range(100):
                #         c = next(f)
                #         if i in [0, 1, 2, 5]:
                #             continue
                #         print(c)
                #         try:
                #             text = c.decode(coding).replace('\u3000\u3000','')
                #         except Exception as e:
                #             print(c,2)
                #         head.append(text.replace('\r\n',''))
                #         if re.search('^[第|一|1|序|自序]',text) and h == '\r\n':
                #             break
                #         h=text
                #
                # print(head)



from api.models import BookTemp,AliyunFileInfo

import rarfile
d = './zxcs_ok'
# d = './books'
file_list = os.listdir(d)
for file in file_list:
    if file.lower().endswith('.rar'):
        if AliyunFileInfo.objects.filter(name__icontains=file, bookfileinfo__isnull=False).count():
            continue
        try:
            auther = file.split('作者：')[-1].split('.')[0]
            book = file.split('》')[0].split('《')[1]
            # zz=BookTemp.objects.filter(name__icontains=file.replace('.rar',''), author__icontains=auther, create_time__isnull=True)

            ddd,xxxxx = read_file(d, file)
            ax=datetime.datetime.strptime("-".join([str(k) for k in ddd[2]]), "%Y-%m-%d-%H-%M-%S")
            default_timezone = timezone.get_default_timezone()
            value = timezone.make_aware(ax+datetime.timedelta(hours=8) , default_timezone)
            BookTemp.objects.create(name=ddd[0].replace('.rar','').replace('.txt',''),size=ddd[1],create_time=value,description=xxxxx
                                    ,author=auther, book_name=book,downloadurl=1)

                # zz.update(name=ddd[0].replace('.rar','').replace('.txt',''),size=ddd[1],create_time=value)

        except Exception as e:
            print(file,e)
        # read_file(d, file)
print(x)