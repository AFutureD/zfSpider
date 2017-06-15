# -*- coding: utf-8 -*-
"""
Created on 2016.12.02
@author: 15999222
"""

from bs4 import BeautifulSoup


def get_GP(responser):
    gpa = responser

    soup = BeautifulSoup(gpa,'html.parser').find(id="Datagrid1").findAll('tr')
    gpa = {'name':'','xf':'','jd':'','ps':'','qz':'','qm':'','cj':''}
    gpa_all = []
    print("contant")

    for line in soup:
        td = line.findAll('td')
        # i = 0
        # for elem in td:
        #     print(i,elem.text)
        #     i += 1
        tmp = gpa.copy()
        tmp['name'] = td[3].text #课程名称
        tmp['xf'] = td[6].text #学分
        tmp['jd'] = td[7].text.replace(u'\xa0', ' ').strip()  #绩点
        tmp['ps'] = td[8].text.replace(u'\xa0', ' ') #平时
        tmp['qz'] = td[9].text.replace(u'\xa0', ' ') #期中
        tmp['qm'] = td[10].text.replace(u'\xa0', ' ') #期末
        tmp['cj'] = td[12].text #成绩
        gpa_all.append(tmp)

    return gpa_all


def get_sch(responser):
    kebiaoOrigin = responser
    cus = -1
    Class ={'course_nature':'','time':'','course_place':'','course_teacher':'','course_name':'','course_id':''}
    class_All = []
    table_nodes = BeautifulSoup(kebiaoOrigin,'html.parser').find(id="Table1").findAll('tr')


    i = 1
    trCu = 1
    for tr in table_nodes:
        trCu += 1
        elem = tr
        for td in elem.findAll('td'):
            if td.text != ' ':
                i += 1
                tdNode = td.get_text('!')
                tmp = tdNode.split('!')

                if len(tmp) >= 2:
                    cls = Class.copy()
                    cus = cus + 1
                    cls['course_name'] = tmp[0]
                    cls['course_nature'] = tmp[1]
                    cls['time'] = tmp[2]
                    cls['course_teacher'] = tmp[3]
                    if len(tmp) >= 5:
                        cls['course_place'] = tmp[4]
                    class_All.append(cls)
        # print()

    return class_All

def get_GPA(responser):
    GPA = responser
    ans = BeautifulSoup(GPA,'html.parser').find_all(id="pjxfjd")[0].get_text()
    return ans

def total_info(responser):
    GPA = responser
    ans = BeautifulSoup(GPA,'html.parser').find(id="Datagrid2").findAll('tr')
    for tr in ans:
        elem = tr
        for td in elem.findAll( 'td' ):
            print(td,end = ' ')
        print()

    #ans = BeautifulSoup(GPA,'html.parser').find_all(id="pjxfjd")[0].get_text()
    return None