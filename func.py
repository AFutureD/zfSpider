# -*- coding: utf-8 -*-
"""
Created on 2016.12.02
@author: 15999222
"""

import re
import parserInfo
from uuid import uuid1
from icalendar import Calendar, Event
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from prettytable import PrettyTable
from database import data_conn
import time

def display(cal):
    return cal.to_ical().decode('utf-8').replace('\r\n', '\n').strip()

def get_ics(schedule):

    # BEGIN:VCALENDAR
    # VERSION:2.0
    # PRODID:-//Apple Inc.//Mac OS X 10.12.1//EN
    # X-WR-TIMEZONE:Asia/Shanghai

    cal = Calendar()
    cal['version'] = '2.0'
    cal['prodid'] = '-//Apple Inc.//Mac OS X 10.12.1//EN'  # *mandatory elements* where the prodid can be changed, see RFC 5445
    cal['X-WR-TIMEZONE'] = 'Asia/Shanghai'

    start_monday = date(2017, 8, 28)  # 开学第一周星期一的时间
    # end_sunday = date(2017, 6, 11)

    dict_week = {'一': 0, '二': 1, '三': 2, '四': 3, '五': 4, '六': 5, '日': 6}
    dict_day = {'1': relativedelta(hours=8, minutes=20), '3': relativedelta(hours=10, minutes=15),
                '5': relativedelta(hours=13, minutes=0), '7': relativedelta(hours=14, minutes=50),
                '9': relativedelta(hours=17, minutes=30)}
    repeat_week = {'单': relativedelta(days=0), '双': relativedelta(days=7)}

    for line in schedule:
        event = Event()

        #      0            1               2       3     4       5        6     7     8      9   10  11
        # ('16209020', 'C语言程序设计', '2015-2016', '1', '李冶', '博文306', '一', '1,2', '5', '18', 0, '')

        start_day = start_monday \
                       + relativedelta(weeks = (int(line[8]) - 1)) \
                       + relativedelta(days = int(dict_week[line[6]]))
        end_day = start_monday \
                       + relativedelta(weeks = (int(line[9]) - 1)) \
                       + relativedelta(days = int(dict_week[line[6]]))

        dtstart_datetime = datetime.combine(start_day, datetime.min.time())
        dtstart = dtstart_datetime + dict_day[line[7][0]]

        dtend = dtstart + relativedelta(hours = 1, minutes = 40)

        # BEGIN:VEVENT -
        # SUMMARY:面向对象的程序设计C++ - 博文309 -
        # DTSTART;VALUE=DATE-TIME:20170228T082000
        # DTEND;VALUE=DATE-TIME:20170228T100000
        # DTSTAMP;VALUE=DATE-TIME:20170113T004630Z
        # UID:ab3f7f5c-d8e6-11e6-93a5-784f4351fe2b@Dong -
        # RRULE:FREQ=WEEKLY;UNTIL=20170611;INTERVAL=1 -
        # CREATED;VALUE=DATE-TIME:20170113T004630Z -
        # END:VEVENT -

        if line[10] == 0:
            interval = 1
        else:
            interval = 2
            dtstart = dtstart + repeat_week[line[11]]
            dtend = dtend + repeat_week[line[11]]
        # 如果有单双周的课 那么这些课隔一周上一次

        event.add('rrule', {'freq': 'weekly', 'interval': interval, 'until': end_day})
        # 设定重复次数

        event.add('created', datetime.now())
        event.add('uid', str(uuid1()) + '@15999222')
        event.add('summary', line[1] + ' - ' + line[5])
        event.add('dtstamp', datetime.now())
        event.add('dtstart', dtstart)
        event.add('dtend', dtend)
        cal.add_component(event)


    return cal


def get_cal(info):
    print("正在获取课程表...")
    schedule = info

    # schedule should be like this:
    #    [{'type': '学必', 'name': 'JAVA程序设计', 'place': '博文205', 'time': '周一第1,2节{第1-18周}', 'teacher': '穆宝良'},
    #     {'type': '学必', 'name': '数字电路数字逻辑', 'place': '软件118', 'time': '周二第1,2节{第1-18周}', 'teacher': '王晓薇'},
    #     {'type': '通必', 'name': '大学外语3', 'place': '汇文509', 'time': '周三第1,2节{第1-18周}', 'teacher': '李静'},
    #     {'type': '学必', 'name': '线性代数', 'place': '博文206', 'time': '周五第3,4节{第1-15周|双周}', 'teacher': '耿莹'},
    #     {'type': '通选', 'name': '教育与生活', 'place': '博文206', 'time': '周四第9,10节{第1-15周}', 'teacher': '蒋春洋'}]

    print("获取成功!")
    print("\n课表是...")

    table = PrettyTable( )
    table.field_names = ['课程名', '课程代码', '类型', '时间', '教师', '地点']
    for line in schedule:
        table.add_row( [ line['course_name'], line['course_id'], line['course_nature'], line['time'], line['course_teacher'], line['course_place'] ] )
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

def show_GP(info):
    gpa_all = info
    table = PrettyTable()
    table.field_names = ['课程名','学分','绩点','平时成绩','期中成绩','期末成绩','最终成绩']
    for line in gpa_all:
        table.add_row([line['name'],line['xf'],line['jd'],line['ps'], line['qz'],line['qm'],line['cj']])
    print(table)

def show_GPA(info):
    print(info)



def format_courses(courses):

    # {'course_term': '(2017-2018-1)-16209460-030018-1', 'course_id': '16209460', 'course_name': '单片机原理与接口技术应用',
    #  'course_nature': '学科必修', 'course_teacher': '李冶', 'course_credit': '5.0',
    #  'course_time': '周一第1,2节{第1-18周};周三第1,2节{第1-18周};周四第1,2节{第1-17周|单周}',
    #  'course_place': '软件120B;软件120B;软件120B'}
    ob_sql = data_conn()
    ob_sql.start()
    conn_new = ob_sql.conn
    cursor = conn_new.cursor()

    tmp_year, tmp_term = re.findall(r'^[(]([\d-]+)-([\d]+)[)]', courses[0]['course_term'])[0]

    cursor.execute("SELECT * FROM course_schedule WHERE course_year = '%s' AND course_term = '%s'" % (tmp_year, tmp_term))
    conn_new.commit()
    tmp_check = cursor.fetchone()
    if tmp_check is not None:
        cursor.execute("delete from course_schedule WHERE course_year = '%s' AND course_term = '%s' " % (tmp_year, tmp_term))
        conn_new.commit()

    print('start to input data into database.')

    for line in courses:
        if line['course_time'] is '':
            continue

        item_id = line['course_id']
        item_name = line['course_name']
        item_nature = line['course_nature']
        item_credit = line['course_credit']
        item_year , item_term  = re.findall(r'^[(]([\d-]+)-([\d]+)[)]', line['course_term'])[0]
        item_teacher = line['course_teacher']
        places = line['course_place']
        item_place = places.split(';')

        # 周三第7,8节{第1-15周};
        # item_start_week = 1
        # item_end_week = 15
        # item_num = 7,8
        # item_day = 三
        # item_odd_dual_bool = 0

        times = line['course_time'].split(';')
        #print(times)
        for index,once in enumerate(times):
            #print(re.findall(r'^[周]([\w]+)第([\d,]+)节{([\w\W]+)}',once))
            item_day,item_num,tmp = re.findall(r'^[周]([\w]+)第([\d,]+)节{([\w\W]+)}',once)[0]
            if '|' in tmp:
                item_odd_dual_bool = 1
                item_start_week,item_end_week,item_odd_dual = re.findall(r'^第([\d]+)-([\d]+)周[|]([\w]+)周',tmp)[0]
            else:
                item_odd_dual_bool = 0
                item_start_week, item_end_week = re.findall(r'^第([\d]+)-([\d]+)周', tmp)[0]
                item_odd_dual = ''

            insert_course_schedule = "insert into course_schedule(course_id,\
                                                                  course_year,\
                                                                  course_term,\
                                                                  course_teacher,\
                                                                  course_place,\
                                                                  course_day,\
                                                                  course_num,\
                                                                  course_start_week,\
                                                                  course_end_week,\
                                                                  course_odd_dual_bool,\
                                                                  course_odd_dual) \
                                                                  values \
                                                                  ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"
            insert_course_info = "insert into courses_info(course_id,\
                                                           course_name,\
                                                           course_nature,\
                                                           course_credit) \
                                                           values \
                                                           ('%s','%s','%s','%s')"

            cursor_if_duplicate = conn_new.cursor()
            cursor_if_duplicate.execute("select * from courses_info where course_id = '%s'" % (item_id))
            #print()
            if cursor_if_duplicate.fetchone() is None:
                cursor.execute(insert_course_info % (item_id, item_name, item_nature, item_credit))

            cursor.execute(insert_course_schedule % (item_id,item_year,item_term,item_teacher,item_place[index],item_day,
                                                     item_num,item_start_week,item_end_week,
                                                     item_odd_dual_bool,item_odd_dual))
            conn_new.commit()

    ob_sql.end()
    print('already input to database')

    return

def format_grades(grades):

    print('start to input data into database.')

    ob_sql = data_conn()
    ob_sql.start()
    conn_new = ob_sql.conn
    cursor = conn_new.cursor()

    tmp_year = grades[0]['grade_year']
    tmp_term = grades[0]['grade_term']

    cursor.execute("SELECT * FROM grades_table WHERE grade_year = '%s' AND grade_term = '%s'" % (tmp_year, tmp_term))
    conn_new.commit()
    tmp_check = cursor.fetchone()
    if tmp_check is not None:
        cursor.execute(
            "delete from grades_table WHERE grade_year = '%s' AND grade_term = '%s' " % (tmp_year, tmp_term))
        conn_new.commit()

    for grade_item in grades:
        insert_grade_table = "insert into grades_table(course_id,\
                                                       grade_year,\
                                                       grade_term,\
                                                       grade_point,\
                                                       grade_regular,\
                                                       grade_midterm,\
                                                       grade_finalexam,\
                                                       grade_total) \
                                                       values('%s','%s','%s','%s','%s','%s','%s','%s')"
        cursor.execute(insert_grade_table % (grade_item['course_id'],grade_item['grade_year'],grade_item['grade_term'],
                                             grade_item['grade_point'],grade_item['grade_regular'],grade_item['grade_midterm'],
                                             grade_item['grade_finalexam'],grade_item['grade_total']))
        conn_new.commit()

    ob_sql.end()
    print('already input to database')

    pass

def show_courses(xn = None,xq = None):


    ob_sql = data_conn()
    ob_sql.start()
    conn_new = ob_sql.conn
    cursor = conn_new.cursor()

    sql_courses = "SELECT courses_info.course_id,\
                          courses_info.course_name,\
                          course_schedule.course_year,\
                          course_schedule.course_term,\
                          course_schedule.course_teacher,\
                          course_schedule.course_place,\
                          course_schedule.course_day,\
                          course_schedule.course_num,\
                          course_schedule.course_start_week,\
                          course_schedule.course_end_week,\
                          course_schedule.course_odd_dual_bool,\
                          course_schedule.course_odd_dual \
                    FROM courses_info,course_schedule \
                    WHERE course_schedule.course_year = '%s' \
                      AND course_schedule.course_term = '%s' \
                      AND course_schedule.course_id=courses_info.course_id"

    cursor.execute(sql_courses % (xn,xq))
    conn_new.commit()
    ob_sql.end()
    courses = cursor.fetchall()


    print("正在生成 ics 文件...")
    ics = get_ics(courses)
    print("生成成功!")

    file_name = 'output.ics'
    print("正在保存到..." + file_name)
    with open(file_name, 'wb') as f:
        f.write(ics.to_ical())
        if f:
            print('保存成功!')
        else:
            print('保存失败!')



    pass


def show_grades(xn = None,xq = None):

    print(xq is '')
    ob_sql = data_conn()
    ob_sql.start()
    conn_new = ob_sql.conn
    cursor = conn_new.cursor()

    if not xq == '':
        sql_courses = "SELECT courses_info.course_id,\
                              courses_info.course_name,\
                              grades_table.grade_year,\
                              grades_table.grade_term,\
                              courses_info.course_credit,\
                              grades_table.grade_point,\
                              grades_table.grade_regular,\
                              grades_table.grade_midterm,\
                              grades_table.grade_finalexam,\
                              grades_table.grade_total \
                      FROM courses_info,grades_table \
                      WHERE grades_table.grade_year = '%s' \
                      AND grades_table.grade_term = '%s' \
                      AND grades_table.course_id=courses_info.course_id"
        cursor.execute(sql_courses % (xn, xq))
    else:
        sql_courses = "SELECT courses_info.course_id,\
                                      courses_info.course_name,\
                                      grades_table.grade_year,\
                                      grades_table.grade_term,\
                                      courses_info.course_credit,\
                                      grades_table.grade_point,\
                                      grades_table.grade_regular,\
                                      grades_table.grade_midterm,\
                                      grades_table.grade_finalexam,\
                                      grades_table.grade_total \
                              FROM courses_info,grades_table \
                              WHERE grades_table.grade_year = '%s' \
                              AND grades_table.course_id=courses_info.course_id"
        cursor.execute(sql_courses % (xn))
    conn_new.commit()
    courses = cursor.fetchall()

    # for line in courses:
    #     print(line)
    ob_sql.end()

    table = PrettyTable()
    table.field_names = ['课程ID', '课程名', '学年', '学期', '学分', '绩点', '平时成绩', '期中成绩', '期末成绩', '最终成绩']
    for line in courses:
        table.add_row([line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7], line[8], line[9]])
    print(table)
    pass