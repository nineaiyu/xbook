#!/usr/bin/env python
# -*- coding:utf-8 -*-
# project : server
# filename : 0002_auto_20230523_1814
# author : ly_13
# date : 5/23/2023

from django.db import migrations

book_label_list = [
    {'name': '仙草', 'label_type': 3}, {'name': '粮草', 'label_type': 3}, {'name': '干草', 'label_type': 3},
    {'name': '枯草', 'label_type': 3}, {'name': '毒草', 'label_type': 3}, {'name': '都市娱乐', 'label_type': 2},
    {'name': '武侠', 'label_type': 2}, {'name': '仙侠', 'label_type': 2}, {'name': '奇幻', 'label_type': 2},
    {'name': '玄幻', 'label_type': 2}, {'name': '科幻', 'label_type': 2}, {'name': '灵异', 'label_type': 2},
    {'name': '历史', 'label_type': 2}, {'name': '军事', 'label_type': 2}, {'name': '竞技', 'label_type': 2},
    {'name': '游戏', 'label_type': 2}, {'name': '二次元', 'label_type': 2}, {'name': '豪门', 'label_type': 1},
    {'name': '孤儿', 'label_type': 1}, {'name': '盗贼', 'label_type': 1}, {'name': '特工', 'label_type': 1},
    {'name': '黑客', 'label_type': 1}, {'name': '明星', 'label_type': 1}, {'name': '特种兵', 'label_type': 1},
    {'name': '杀手', 'label_type': 1}, {'name': '老师', 'label_type': 1}, {'name': '学生', 'label_type': 1},
    {'name': '展开', 'label_type': 1}, {'name': '胖子', 'label_type': 1}, {'name': '宠物', 'label_type': 1},
    {'name': '蜀山', 'label_type': 1}, {'name': '魔王附体', 'label_type': 1}, {'name': 'LOL', 'label_type': 1},
    {'name': '废材流', 'label_type': 1}, {'name': '护短', 'label_type': 1}, {'name': '卡片', 'label_type': 1},
    {'name': '手游', 'label_type': 1}, {'name': '法师', 'label_type': 1}, {'name': '医生', 'label_type': 1},
    {'name': '感情', 'label_type': 1}, {'name': '鉴宝', 'label_type': 1}, {'name': '亡灵', 'label_type': 1},
    {'name': '职场', 'label_type': 1}, {'name': '吸血鬼', 'label_type': 1}, {'name': '龙', 'label_type': 1},
    {'name': '西游', 'label_type': 1}, {'name': '鬼怪', 'label_type': 1}, {'name': '阵法', 'label_type': 1},
    {'name': '魔兽', 'label_type': 1}, {'name': '勇猛', 'label_type': 1}, {'name': '玄学', 'label_type': 1},
    {'name': '群穿', 'label_type': 1}, {'name': '丹药', 'label_type': 1}, {'name': '练功流', 'label_type': 1},
    {'name': '召唤流', 'label_type': 1}, {'name': '恶搞', 'label_type': 1}, {'name': '爆笑', 'label_type': 1},
    {'name': '轻松', 'label_type': 1}, {'name': '冷酷', 'label_type': 1}, {'name': '腹黑', 'label_type': 1},
    {'name': '阳光', 'label_type': 1}, {'name': '狡猾', 'label_type': 1}, {'name': '机智', 'label_type': 1},
    {'name': '猥琐', 'label_type': 1}, {'name': '嚣张', 'label_type': 1}, {'name': '淡定', 'label_type': 1},
    {'name': '僵尸', 'label_type': 1}, {'name': '丧尸', 'label_type': 1}, {'name': '盗墓', 'label_type': 1},
    {'name': '随身流', 'label_type': 1}, {'name': '软饭流', 'label_type': 1}, {'name': '无敌文', 'label_type': 1},
    {'name': '异兽流', 'label_type': 1}, {'name': '系统流', 'label_type': 1}, {'name': '洪荒流', 'label_type': 1},
    {'name': '学院流', 'label_type': 1}, {'name': '位面', 'label_type': 1}, {'name': '铁血', 'label_type': 1},
    {'name': '励志', 'label_type': 1}, {'name': '坚毅', 'label_type': 1}, {'name': '变身', 'label_type': 1},
    {'name': '强者回归', 'label_type': 1}, {'name': '赚钱', 'label_type': 1}, {'name': '争霸流', 'label_type': 1},
    {'name': '种田文', 'label_type': 1}, {'name': '宅男', 'label_type': 1}, {'name': '无限流', 'label_type': 1},
    {'name': '技术流', 'label_type': 1}, {'name': '凡人流', 'label_type': 1}, {'name': '热血', 'label_type': 1},
    {'name': '重生', 'label_type': 1}, {'name': '穿越', 'label_type': 1}
]


def add_default_book_label(apps, schema_editor):
    for price in book_label_list:
        price_model = apps.get_model('api', 'BookLabels')
        price_model.objects.create(**price)


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_default_book_label),
    ]
