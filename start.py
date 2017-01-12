# -*- coding: utf-8 -*-
"""
Created on 2016.12.02
@author: 15999222
"""

import func
import parserInfo
from spider import Student

if __name__ == "__main__":
    ob = Student(num = '15999222',password = 'dhn78834',name = '董华楠')
    ob.login()
    while 1:
        switch = input("输入 1：获取课表并转为ical\t 2：查询学期成绩\t 0：结束\n")
        # print(switch)
        if switch == '0':
            break
        if switch == '1':
            responser = ob.sp_class()
            info = parserInfo.get_sch(responser)
            func.get_cal(info)
        if switch == '2':
            responser = ob.sp_GPA()
            info = parserInfo.get_GPA(responser)
            func.show_GPA(info)


