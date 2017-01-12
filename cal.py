# -*- coding: utf-8 -*-
"""
Created on 2016.12.02
@author: 15999222
"""

import re
from uuid import uuid1
from prettytable import PrettyTable
from icalendar import Calendar, Event
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import parserInfo

def display(cal):
    return cal.to_ical().decode('utf-8').replace('\r\n', '\n').strip()


def get_ics(schedule):


    """
    BEGIN:VCALENDAR
    METHOD:PUBLISH
    VERSION:2.0 // <
    X-WR-CALNAME:课程表
    PRODID:-//Apple Inc.//Mac OS X 10.12.1//EN // <
    X-APPLE-CALENDAR-COLOR:#FF2968
    X-WR-TIMEZONE:Asia/Shanghai <
    CALSCALE:GREGORIAN
    """

    cal = Calendar()
    cal['version'] = '2.0'
    cal['prodid'] = '-//Apple Inc.//Mac OS X 10.12.1//EN'  # *mandatory elements* where the prodid can be changed, see RFC 5445
    cal['X-WR-TIMEZONE'] = 'Asia/Shanghai'

    start_monday = date(2017, 2, 27)  # 开学第一周星期一的时间
    end_sunday = date(2017, 6, 11)
    dict_week = {'一': 0, '二': 1, '三': 2, '四': 3, '五': 4, '六': 5, '日': 6}
    dict_day = {1: relativedelta(hours=8, minutes=20), 3: relativedelta(hours=10, minutes=15),
                5: relativedelta(hours=13, minutes=0), 7: relativedelta(hours=14, minutes=50),
                9: relativedelta(hours=17, minutes=30)}
    repeat_week = {'单': relativedelta(days=0), '双': relativedelta(days=7)}

    for line in schedule:
        event = Event()
        # print(line)
        # line should be like this: ['汇编语言程序设计', '周三第7,8节', '第10-10周|双周', '第1实验楼B403-A', '刘小洋(刘小洋)']

        info_day = re.findall(r'周(.*?)第(\d+),(\d+)节', line['time'])
        info_day = info_day[0]
        # print(info_day)
        # info_day should be like this: ('三', '7', '8')

        info_week = re.findall(r'第(\d+)-(\d+)周', line['time'])
        info_week = info_week[0]
        # print(info_week)
        # info_week should be like this: ('10', '10')

        dtstart_date = start_monday + relativedelta(weeks=(int(info_week[0]) - 1)) + relativedelta(days=int(dict_week[info_day[0]]))
        dtstart_datetime = datetime.combine(dtstart_date, datetime.min.time())
        dtstart = dtstart_datetime + dict_day[int(info_day[1])]

        dtend = dtstart + relativedelta(hours=1, minutes=40)

            # BEGIN:VEVENT
            # CREATED:20160707T102231Z <
            # UID:82EA36A8-A6D9-4F72-ADC4-EB365500BC01 <
            # RRULE:FREQ=WEEKLY;INTERVAL=2;UNTIL=20170101T155959Z //interval 表示时间间隔
            # DTEND;TZID=Asia/Shanghai:20160909T115000
            # TRANSP:OPAQUE
            # X-APPLE-TRAVEL-ADVISORY-BEHAVIOR:AUTOMATIC
            # SUMMARY:博文206 - 线性代数
            # DTSTART;TZID=Asia/Shanghai:20160909T101500
            # DTSTAMP:20160707T102232Z
            # LAST-MODIFIED:20160707T102231Z
            # SEQUENCE:0
            # END:VEVENT

        repeat = re.findall(r'\|(.*?)周', line['time'])
        if len(repeat) == 0:
            interval = 1
            # print("yes")
        else:
            # print("NO")
            interval = 2
            # print(repeat)
            dtstart = dtstart + repeat_week[repeat[0]]
            dtend = dtend + repeat_week[repeat[0]]
        # 如果有单双周的课 那么这些课隔一周上一次

        event.add('rrule',
                  {'freq': 'weekly', 'interval': interval,
                   'until': end_sunday})
        # 设定重复次数

        event.add('created', datetime.now())
        event.add('uid', str(uuid1()) + '@Dong')
        event.add('summary', line['name'] + ' - ' + line['place'])
        event.add('dtstamp', datetime.now())
        event.add('dtstart', dtstart)
        event.add('dtend', dtend)
        cal.add_component(event)
    return cal


def get_cal(ob):
    print("正在获取课程表...")
    schedule = parserInfo.get_sch(ob)

    # schedule should be like this:
    #    [{'type': '学必', 'name': 'JAVA程序设计', 'place': '博文205', 'time': '周一第1,2节{第1-18周}', 'teacher': '穆宝良'},
    #     {'type': '学必', 'name': '数字电路数字逻辑', 'place': '软件118', 'time': '周二第1,2节{第1-18周}', 'teacher': '王晓薇'},
    #     {'type': '通必', 'name': '大学外语3', 'place': '汇文509', 'time': '周三第1,2节{第1-18周}', 'teacher': '李静'},
    #     {'type': '学必', 'name': '线性代数', 'place': '博文206', 'time': '周一第3,4节{第1-15周}', 'teacher': '耿莹'},
    #     {'type': '通必', 'name': '体育3', 'place': '', 'time': '周四第3,4节{第1-18周}', 'teacher': '王瑾'},
    #     {'type': '学必', 'name': '线性代数', 'place': '博文206', 'time': '周五第3,4节{第1-15周|双周}', 'teacher': '耿莹'},
    #     {'type': '学必', 'name': '数字电路数字逻辑', 'place': '博文409', 'time': '周三第5,6节{第1-18周}', 'teacher': '王晓薇'},
    #     {'type': '学必', 'name': 'JAVA程序设计', 'place': '博文106', 'time': '周四第5,6节{第1-18周}', 'teacher': '穆宝良'},
    #     {'type': '通必', 'name': '大学外语3', 'place': '汇文509', 'time': '周一第7,8节{第1-18周}', 'teacher': '李静'},
    #     {'type': '学必', 'name': '数据结构', 'place': '博文401', 'time': '周二第7,8节{第1-18周}', 'teacher': '穆宝良'},
    #     {'type': '学必', 'name': '专业外语', 'place': '博文309', 'time': '周三第7,8节{第1-15周}', 'teacher': '崔黎黎'},
    #     {'type': '学必', 'name': '数据结构', 'place': '博文201', 'time': '周四第7,8节{第1-18周}', 'teacher': '穆宝良'},
    #     {'type': '学必', 'name': '专业外语', 'place': '博文102', 'time': '周五第7,8节{第1-15周}', 'teacher': '崔黎黎'},
    #     {'type': '通选', 'name': '学在旅途 实用英语', 'place': '博文305', 'time': '周三第9,10节{第1-15周}', 'teacher': '孔瑜'},
    #     {'type': '通选', 'name': '教育与生活', 'place': '博文206', 'time': '周四第9,10节{第1-15周}', 'teacher': '蒋春洋'}]

    print("获取成功!")
    print("\n课表是...")

    table = PrettyTable( )
    table.field_names = ['课程名', '类型', '时间', '教师', '地点']
    for line in schedule:
        table.add_row( [ line['name'], line['type'], line['time'], line['teacher'], line['place'] ] )
    print( table )

    print("\n正在生成 ics 文件...")
    ics = get_ics(schedule)
    # print(display(ics))
    print("生成成功!")

    file_name = 'output.ics'
    print("\n正在保存到..." + file_name)
    with open(file_name, 'wb') as f:
        f.write(ics.to_ical())
        if f:
            print('保存成功!')
        else:
            print('保存失败!')
