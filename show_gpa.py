# -*- coding: utf-8 -*-
"""
Created on 2016.12.02
@author: 15999222
"""

import parserInfo
from prettytable import PrettyTable
def show_GPA(ob):
	gpa_all = parserInfo.get_GPA(ob)
	table = PrettyTable()
	table.field_names = ['课程名','学分','绩点','平时成绩','期中成绩','期末成绩','最终成绩']
	for line in gpa_all:
		table.add_row([line['name'],line['xf'],line['jd'],line['ps'], line['qz'],line['qm'],line['cj']])
	print(table)