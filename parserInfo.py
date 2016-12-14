# -*- coding: utf-8 -*-
"""
Created on 2016.12.02
@author: 15999222
"""

from bs4 import BeautifulSoup

def get_GPA(ob):
    
    # DstDir = os.getcwd() + "/"
    # with open(DstDir + "gpa.txt","rb") as a:
    #     gpa = a.read()

    gpa = ob.sp_GPA()

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

def get_sch(ob):
    
    # DstDir = os.getcwd() + "/"
    # with open(DstDir + "kebiao.html","rb") as a:
    #     kebiaoOrigin = a.read()

    kebiaoOrigin = ob.sp_Class()
    cus = -1
    Class ={'type':'','time':'','place':'','teacher':'','name':''}
    class_All = []
    table_nodes = BeautifulSoup(kebiaoOrigin,'html.parser',from_encoding = 'utf8').find(id="Table1").findAll('tr')


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
                    cls['name'] = tmp[0]
                    cls['type'] = tmp[1]
                    cls['time'] = tmp[2]
                    cls['teacher'] = tmp[3]
                    if len(tmp) >= 5:
                        cls['place'] = tmp[4]
                    class_All.append(cls)
        # print()

    return class_All