#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2016.12.02
@author: 15999222
"""

import func
import parserInfo
from spider import Student
# import command
import json



def main():

    with open('json/base_info.json') as json_file:
        base_data = json.load(json_file)
    jiaowu_data = base_data['jiaowu']

    ob = Student(num = jiaowu_data['stu_number'],password = jiaowu_data['stu_passwd'],pic2Num = jiaowu_data['pic2Num'])
    ob.login() # login function,in order to log in the system.
    ob.get_ess()
    ob.latest_login_time()


    while 1:
        switch = input("\n输入 \n"
                       "1：获取课表并转为ical\t "
                       "2：查询学期成绩\t "
                       "3：查询平均学分绩点\t "
                       "4:更新数据\t "
                       "0：结束\n")

        if switch == '0':
            break
        if switch == '1':
            xn, xq = ob.choices(info = 'course', type = 1)
            func.show_courses(xn, xq)

        if switch == '2':
            xn, xq = ob.choices(info = 'grade', type = 0)
            func.show_grades(xn, xq)

        if switch == '3':
            responser = ob.sp_GPA()
            GPA = parserInfo.get_GPA(responser)
            func.show_GPA(GPA)

        if switch == '4':
            ob.update_all_info()

    return 0

if __name__ == "__main__":
    main()


