# -*- coding: utf-8 -*-
"""
Created on 2016.12.02
@author: 15999222
"""

import cal
import spider
import show_gpa

if __name__ == "__main__":
    ob = spider.Student()
    ob.login()
    while 1:
        switch = input("输入 1：获取课表并转为ical\t 2：查询学期成绩\t 0：结束\n")
        # print(switch)
        if switch == '0':
            break
        if switch == '1':
            cal.get_cal(ob)
        if switch == '2':
            show_gpa.show_GPA( ob )


