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

def get_courses_schedule(responser):

    soup = BeautifulSoup(responser, 'html.parser')
    a = soup.find(id = 'DBGrid').find_all('tr')

    course_item ={'course_term':'',
                  'course_id':'',
                  'course_name':'',
                  'course_nature':'',
                  'course_teacher':'',
                  'course_credit':'',
                  'course_time': '',
                  'course_place':''
        }
    courses = []


    for i,item in enumerate(a):
        if i == 0:
            continue
        #print(item)
        tds = item.findAll('td')
        # for index,td in enumerate(tds):
        course_tmp = course_item.copy()
        course_tmp['course_term'] = tds[0].get_text()
        course_tmp['course_id'] = tds[1].get_text()
        course_tmp['course_name'] = tds[2].get_text()
        course_tmp['course_nature'] = tds[3].get_text().replace('\xa0','')
        course_tmp['course_teacher'] = tds[5].get_text()
        course_tmp['course_credit'] = tds[6].get_text()
        course_tmp['course_time'] = tds[8].get_text().replace('\n','')
        course_tmp['course_place'] = tds[9].get_text().replace('\xa0','')
        courses.append(course_tmp)

    # for a in courses:
    #     print(a)

    return courses

def get_grades(responser):

    soup = BeautifulSoup(responser, 'html.parser').find(id = "Datagrid1").findAll('tr')
    grade_item = {'grade_year' : '',
           'grade_term' : '',
           'course_id' : '',
           'course_name' : '',
           'grade_credit' : '',
           'grade_point' : '',
           'grade_regular' : '',
           'grade_midterm' : '',
           'grade_finalexam' : '',
           'grade_total' : ''
    }
    grades = []

    for index,line in enumerate(soup):
        if index == 0:
            continue
        td = line.findAll('td')
        tmp = grade_item.copy()
        tmp['grade_year'] = td[0].text
        tmp['grade_term'] = td[1].text
        tmp['course_id'] = td[2].text
        tmp['course_name'] = td[3].text  # 课程名称
        tmp['grade_credit'] = td[6].text  # 学分
        tmp['grade_point'] = td[7].text.replace(u'\xa0', '0').strip()  # 绩点
        tmp['grade_regular'] = td[8].text.replace(u'\xa0', '')  # 平时
        tmp['grade_midterm'] = td[9].text.replace(u'\xa0', '')  # 期中
        tmp['grade_finalexam'] = td[10].text.replace(u'\xa0', '')  # 期末
        tmp['grade_total'] = td[12].text  # 成绩
        grades.append(tmp)

    return grades