# -*- coding: utf-8 -*-
"""
Created on 2016.12.02
@author: 15999222
"""

import platform
import os
import re
import requests
from urllib.parse import quote
from bs4 import BeautifulSoup

XN = ["2015-2016","2016-2017"]
XQ = ["1", "2"]
IFLOGIN = "请登录"


class Student:
    def __init__(self,num = None,password = None):
        self.st_num = num  # 学号
        self.st_password = password  # 密码
        self.st_name = None  # 姓名
        self.st_urlName = None  # url编码后的姓名
        # print(self.st_urlName)
        self.session = requests.session()
        self.baseUrl = "http://210.30.208.140/"
        self.avail_courses_year = []
        self.avail_courses_term = []
        self.avail_grade_year = []
        self.avail_grade_term = []
        self.__VIEWSTATE2 = None
        self.__VIEWSTATE3 = None

    def login(self):
        # 访问教务系统
        status = True
        print("正在尝试登录......")
        self.session.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
        response = self.session.get(self.baseUrl)
        self.baseUrl = response.url
        self.baseUrl = re.subn(r'.default2.aspx', '', self.baseUrl)[0]
        loginUrl = self.baseUrl + '/default2.aspx'

        while (status):
            response = self.session.get(loginUrl)
            __VIEWSTATE = re.findall("name=\"__VIEWSTATE\" value=\"(.*?)\"", response.content.decode('GBK'))[0]
            # print(__VIEWSTATE)
            print("Got viewatate")
            print( "正在获取验证码......" )
            imgUrl = self.baseUrl + "/CheckCode.aspx?"
            imgresponse = self.session.get(imgUrl, stream=True)
            image = imgresponse.content

            # 保存code
            if 'Linux' in platform.system():
                DstDir = os.getcwd() + "/"
                # print(DstDir)
                with open(DstDir + "code.jpg", "wb") as jpg:
                    jpg.write(image)
                    print("保存验证码到：" + DstDir + "code.jpg" + "\n")
                os.popen("display " + DstDir + "code.jpg")

            elif 'windows' in platform.system():
                DstDir = os.getcwd() + "\\"
                print(DstDir)
                with open(DstDir + "code.jpg", "wb") as jpg:
                    jpg.write(image)
                    print("保存验证码到：" + DstDir + "code.jpg" + "\n")
                command = "start" + " \"\" " + DstDir +"code.jpg"
                os.popen( command ).read()
            elif 'Darwin' in platform.system():
                DstDir = os.getcwd() + "/"
                # print(DstDir)
                with open(DstDir + "code.jpg", "wb") as jpg:
                    jpg.write(image)
                    print("保存验证码到：" + DstDir + "code.jpg" + "\n")
                os.popen("open " + DstDir + "code.jpg")

            code = input("验证码是：")
            RadioButtonList1 = u"学生".encode('gb2312', 'replace')
            data = {
                "RadioButtonList1": RadioButtonList1,
                "__VIEWSTATE": __VIEWSTATE,
                "txtUserName": self.st_num,
                "TextBox2": self.st_password,
                "Button1": "",
                "txtSecretCode": code,
            }

            Loginresponse = self.session.post(loginUrl, data=data)
            print("尝试登录中......")

            url2 = self.baseUrl + "/xs_main.aspx?xh=" + self.st_num
            self.session.headers['Referer'] = self.baseUrl + "default2.aspx"
            response2 = self.session.get(url2)
            html = response2.content.decode("gb2312")
            soup = BeautifulSoup(html, 'html.parser')
            title = soup.title.get_text()
            print(title)
            if title.find(IFLOGIN) != -1:  # To determine whether the login is successful
                print("登录失败，正在重新登录......")
                IFCONTINUE = input("输入 0 以结束")
                if IFCONTINUE == '0':
                    break
            else:
                self.st_name = re.findall(r'<span id="xhxm">([\w\W]+)同学</span>',str(soup.find(id="xhxm")))[0]
                self.ECname()
                status = False

        if not status:
            print("成功登录教务系统")
        else:
            print("登录教务系统终止！！！")
        return 1

    def ECname(self):
        self.st_urlName = quote(self.st_name.encode('gb2312'))
        return

    def get_ess(self):

        # 从课程便初始页面获取__VIEWSTATE 可选择的学年和学期可选项

        url2 = self.baseUrl + "/xskbcx.aspx?xh=" + self.st_num + "&xm=" + self.st_urlName + "&gnmkdm=N121603"
        self.session.headers[ 'Referer' ] = self.baseUrl + '/xs_main.aspx?xh=' + self.st_num
        response2 = self.session.get(url2)
        html = response2.content.decode("gb2312")
        soup = BeautifulSoup( html, 'html.parser')
        self.__VIEWSTATE2 = soup.findAll('input')[2]['value']
        self.avail_courses_year = [item.get_text() for item in soup.find(id = 'xnd').find_all('option')]
        self.avail_courses_term = [item.get_text() for item in soup.find(id = 'xqd').find_all('option')]

        url3_1 = self.baseUrl + "/xscjcx.aspx?xh=" + self.st_num + "&xm=" + self.st_urlName + "&gnmkdm=N121605"
        self.session.headers['Referer'] = self.baseUrl + '/xs_main.aspx?xh=' + self.st_num
        response3_1 = self.session.get(url3_1)
        html = response3_1.content.decode("gb2312")
        soup = BeautifulSoup(html, 'html.parser')
        self.__VIEWSTATE3 = soup.findAll('input')[2]['value']
        self.avail_grade_year = [item.get_text() for item in soup.find(id = 'ddlXN').find_all('option')]
        self.avail_grade_year.remove('')
        self.avail_grade_term = [item.get_text() for item in soup.find(id = 'ddlXQ').find_all('option')]
        self.avail_grade_term.remove('')

        # print(self.avail_grade_year)
        # print(self.avail_grade_term)

        print("Got essential information.")
        pass

    def ptch( self, year = None, term = None ):

        print()
        for index,ayear in enumerate(year):
            print('\t{0}:第{1}学年'.format(index+1,ayear), end = ' ')
        print()

        for index,aterm in enumerate(term):
            print('\t{0:}:第{1}{2:<12}'.format(index+1,aterm,'学期'), end = ' ')
        print(end = '\n\n')

        pass

    '''
        个人课表
    '''
    def sp_class(self, year=None, term = None):
        # 选择学期

        self.ptch(year,term)

        choice = int(input("请选择学年：\n"))
        xn = self.avail_courses_year[int(choice)-1]
        choice = int(input("请选择学年：\n"))
        xq = self.avail_courses_term[int(choice)-1]
        print(xn,xq)

        self.session.headers['Referer'] = self.baseUrl + "/xskbcx.aspx?xh=" + self.st_num + "&xm=" + self.st_urlName + "&gnmkdm=N121603"
        data2 = {
            '__EVENTTARGET':'xqd',
            '__EVENTARGUMENT':'',
            '__VIEWSTATE':self.__VIEWSTATE2,
            'xnd':xn,
            'xqd':xq,
        }
        url2 = self.baseUrl + "/xskbcx.aspx?xh=" + self.st_num + "&xm=" + self.st_urlName + "&gnmkdm=N121603"
        response2 = self.session.get(url2,data = data2)
        ans = response2.content.decode('GBK')
        # print(ans)
        return ans

    '''
    GPA
    '''
    def sp_GP(self):
        # 选择学期
        self.ptch(self.avail_grade_year, self.avail_grade_term)

        while 1:
            choice = input("请选择学年：\n")
            if choice is not '':
                try:
                    xn = self.avail_grade_year[int(choice) - 1]
                    break
                except:
                    print("请输入数字")
                    continue

        while 1:
            choice = input("请选择学期：\n")
            if choice is not '':
                try:
                    xq = self.avail_grade_term[int(choice) - 1]
                    break
                except:
                    print("请输入数字")
                    continue

        url3_1 = self.baseUrl + "/xscjcx.aspx?xh=" + self.st_num + "&xm=" + self.st_urlName + "&gnmkdm=N121605"
        self.session.headers['Referer'] = self.baseUrl + "/xscjcx.aspx?xh=" + self.st_num + "&xm=" + self.st_urlName + "&gnmkdm=N121605"
        data3 = {
            "__EVENTTARGET":"",
            "__EVENTARGUMENT":"",
            "__VIEWSTATE":self.__VIEWSTATE3,
            'hidLanguage':"",
            "ddlXN":xn,
            "ddlXQ":xq,
            "ddl_kcxz":"",
            "btn_xq" : u"学期成绩".encode('gb2312', 'replace')
        }
        response3 = self.session.post(url3_1,data=data3)

        ans = response3.content.decode('GBK')
        return ans

    '''
    GPA
    '''

    def sp_GPA(self):
        # 选择学期
        self.ptch(self.avail_grade_year, self.avail_grade_term)

        while 1:
            choice = input("请选择学年：\n")
            if choice is not '':
                try:
                    xn = self.avail_grade_year[int(choice) - 1]
                    break
                except:
                    print("请输入数字")
                    continue

        while 1:
            choice = input("请选择学期（可不输入）：\n")
            if choice is not '':
                try:
                    xq = self.avail_grade_term[int(choice) - 1]
                    break
                except:
                    print("请输入数字")
                    continue
            else:
                xq = ''
                break
        # choice = int(input("请选择学年：\n"))
        # xn = self.avail_grade_year[int(choice) - 1]
        # choice = int(input("请选择学年：\n"))
        # xq = self.avail_grade_term[int(choice) - 1]

        print(xn, xq)

        url3_1 = self.baseUrl + "/xscjcx.aspx?xh=" + self.st_num + "&xm=" + self.st_urlName + "&gnmkdm=N121605"
        self.session.headers['Referer'] = self.baseUrl + "/xscjcx.aspx?xh=" + self.st_num + "&xm=" + self.st_urlName + "&gnmkdm=N121605"
        data3 = {"__EVENTTARGET": "",
                 "__EVENTARGUMENT": "",
                 "__VIEWSTATE": self.__VIEWSTATE3,
                 'hidLanguage': "",
                "ddlXN": xn,
                 "ddlXQ": xq,
                 "ddl_kcxz": "",
                 "Button1": u"成绩统计".encode('gb2312', 'replace')}
        response3 = self.session.post(url3_1, data=data3)

        ans = response3.content.decode('GBK')
        return ans

    def test(self):
        # 选择学期
        choice = int(
            input( "清选择学期：\n\t\t1、2015-2016 第一学期\t2、2015-2016 第二学期\n\t\t3、2016-2017 第一学期\t4、2016-2017 第二学期\n" ) )
        xn = XN[int( (choice - 1) / 2 )]
        xq = XQ[int( (choice - 1) % 2 )]

        url3_1 = self.baseUrl + "/xscjcx.aspx?xh=" + self.st_num + "&xm=" + self.st_urlName + "&gnmkdm=N121605"
        self.session.headers['Referer'] = self.baseUrl + '/xs_main.aspx?xh=' + self.st_num
        response3_1 = self.session.get( url3_1 )
        html = response3_1.content.decode( "gb2312" )
        soup = BeautifulSoup( html, 'html.parser' )
        __VIEWSTATE3 = soup.findAll( 'input' )[2]['value']

        self.session.headers['Referer'] = self.baseUrl + "/xscjcx.aspx?xh=" + self.st_num + "&xm=" + self.st_urlName + "&gnmkdm=N121605"

        data3 = {"__EVENTTARGET": "",
                 "__EVENTARGUMENT": "",
                 "__VIEWSTATE": __VIEWSTATE3,
                 'hidLanguage': "",
                 "ddlXN": xn,
                 "ddlXQ": xq,
                 "ddl_kcxz": "",
                 "Button1": u"成绩统计".encode( 'gb2312', 'replace' )}
        response3 = self.session.post( url3_1, data = data3 )

        ans = response3.content.decode( 'GBK' )

        return ans
