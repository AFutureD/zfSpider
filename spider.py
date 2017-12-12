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
import parserInfo
import func
from database import data_conn
import datetime
from PIL import Image
import json
import warnings
warnings.filterwarnings("ignore")

IFLOGIN = "请登录"


class Student:
    def __init__(self,num = None,password = None,pic2Num = None):
        self.st_num = num  # 学号
        self.st_password = password  # 密码
        self.st_name = None  # 姓名
        self.st_urlName = None  # url编码后的姓名
        self.session = requests.session()
        self.baseUrl = "http://210.30.208.140/"
        self.url2Num = pic2Num
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
        self.session.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        response = self.session.get(self.baseUrl)
        self.baseUrl = response.url
        self.baseUrl = re.subn(r'.default2.aspx', '', self.baseUrl)[0]
        loginUrl = self.baseUrl + '/default2.aspx'

        while (status):
            response = self.session.get(loginUrl)
            __VIEWSTATE = re.findall("name=\"__VIEWSTATE\" value=\"(.*?)\"", response.content.decode('GBK'))[0]
            # print(__VIEWSTATE)
            # print("Got viewatate")
            print( "正在获取验证码......" )
            imgUrl = self.baseUrl + "/CheckCode.aspx?"
            imgresponse = self.session.get(imgUrl, stream=True)
            image = imgresponse.content

            # 保存code
            DstDir = None
            if 'Linux' in platform.system():
                DstDir = os.getcwd() + "/" + "code.jpeg"
                # print(DstDir)
                with open(DstDir, "wb") as jpg:
                    jpg.write(image)
                    print("保存验证码到：" + DstDir)
                os.popen("display " + DstDir)
            elif 'windows' in platform.system():
                DstDir = os.getcwd() + "\\" + "code.jpeg"
                # print(DstDir)
                with open(DstDir, "wb") as jpg:
                    jpg.write(image)
                    print("保存验证码到：" + DstDir)
                command = "start" + " \"\" " + DstDir
                os.popen( command ).read()
            elif 'Darwin' in platform.system():
                DstDir = os.getcwd() + "/" + "code.jpeg"
                # print(DstDir)
                with open(DstDir, "wb") as jpg:
                    jpg.write(image)
                    print("保存验证码到：" + DstDir)
                # os.popen("open " + DstDir)

            # code = input("验证码是：")
            im = Image.open(DstDir)
            im = im.convert('RGB')
            im.save(DstDir, 'jpeg')
            # print(DstDir)

            code = ''
            with open('code.jpeg', 'rb') as codeFile:
                postFile = {'attachment_file': ('code.jpeg', codeFile, 'image/png', {})}
                r1 = requests.post(self.url2Num, files = postFile)
                code = (json.loads(r1.text))['code']

            print(code)
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
            ob_sql = data_conn()
            ob_sql.start()
            conn_new = ob_sql.conn
            cursor = conn_new.cursor()
            cursor.execute("select * from login_info WHERE stu_id = '%s'" % self.st_num)
            now_time = datetime.date.today().isoformat()
            if cursor.fetchone() is None:
                cursor.execute("insert into login_info(stu_id,stu_passwd,login_time) \
                                VALUES ('%s','%s','%s')" % (self.st_num,self.st_password,now_time))
            else:
                cursor.execute("delete from login_info where stu_id = '%s' " % self.st_num)
                cursor.execute("insert into login_info(stu_id,stu_passwd,login_time) \
                                            VALUES ('%s','%s','%s')" % (self.st_num, self.st_password, now_time))
            conn_new.commit()
            ob_sql.end()
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

        url_info_course_schedule = self.baseUrl + "/xsxkqk.aspx?xh=" + self.st_num + "&xm=" + self.st_urlName + "&gnmkdm=N121615"
        self.session.headers['Referer'] = self.baseUrl + '/xs_main.aspx?xh=' + self.st_num
        response2 = self.session.get(url_info_course_schedule)
        html = response2.content.decode("gb2312")
        soup = BeautifulSoup(html, 'html.parser')
        self.__VIEWSTATE_info_course_schedule = soup.findAll('input')[2]['value']

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

    def latest_login_time(self):

        ob_sql = data_conn()
        ob_sql.start()
        conn_new = ob_sql.conn
        cursor = conn_new.cursor()
        cursor.execute("select login_time from login_info WHERE stu_id = '%s'" % self.st_num)
        conn_new.commit()
        time_info = cursor.fetchone()
        ob_sql.end()

        return time_info[0]

    def update_all_info( self ):

        formatter_string = "%y-%m-%d"
        time_info = self.latest_login_time()
        time_info = date_time = datetime.datetime.strptime(time_info,'%Y-%m-%d')
        time_info = time_info.date()
        print(time_info)
        now_time = datetime.date.today()

        if (now_time - time_info).days < 2:
            while 1:
                ans = input("是否刷新数据？(y/n)\n")
                if ans == 'y':
                    print("开始更新所有数据 ......")
                    break
                elif ans == 'n':
                    return
                else:
                    continue
        print("开始更新课表")
        for year in self.avail_courses_year:
            for term in self.avail_courses_term:
                print("更新第%s学年第%s学期中......" % (year,term))
                responser  = self.sp_courses_schedule(year,term)
                courses = parserInfo.get_courses_schedule(responser)
                if courses == []:
                    continue
                # print(courses)
                func.format_courses(courses)
        print("课表更新完成")

        print("开始更新成绩")
        for year in self.avail_grade_year:
            for term in self.avail_grade_term:
                print("更新第%s学年第%s学期中......" % (year, term))
                responser = self.sp_grades(year, term)
                grades = parserInfo.get_grades(responser)
                if grades == []:
                    continue
                func.format_grades(grades)
                # print(grades)
        print("成绩更新完成")


        pass

    def choices( self,info = 'course' , type  = 1):
        '''info can only choice from course or grade, all of them must be a str'''

        year = None; term = None
        if info == 'course':
            year = self.avail_courses_year
            term = self.avail_courses_term
        elif info == 'grade':
            year = self.avail_grade_year
            term = self.avail_grade_term

        print()
        for index,ayear in enumerate(year):
            print('\t{0}:第{1}学年'.format(index+1,ayear), end = ' ')
        print()

        for index,aterm in enumerate(term):
            print('\t{0:}:第{1}{2:<12}'.format(index+1,aterm,'学期'), end = ' ')
        print(end = '\n\n')


        while 1:
            choice = input("请选择学年：\n")
            if choice is not '':
                try:
                    xn = year[int(choice) - 1]
                    break
                except:
                    print("请输入数字")
                    continue
        if type == 1:
            while 1:
                choice = input("请选择学期：\n")
                if choice is not '':
                    try:
                        xq = term[int(choice) - 1]
                        break
                    except:
                        print("请输入数字")
                        continue
        else:
            while 1:
                choice = input("请选择学期（可不输入）：\n")
                if choice is not '':
                    try:
                        xq = term[int(choice) - 1]
                        break
                    except:
                        print("请输入数字")
                        continue
                else:
                    xq = ''
                    break

        return xn,xq

    def sp_grades(self,xn = None,xq = None):
        # 选择学期

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
        return ans.encode('utf-8')

    def sp_GPA(self,xn = None,xq = None):
        # 选择学期
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

    def sp_courses_schedule(self,xn = None,xq = None):

        self.session.headers[
            'Referer'] = self.baseUrl + "/xsxkqk.aspx?xh=" + self.st_num + "&xm=" + self.st_urlName + "&gnmkdm=N121615"
        data2 = {
            '__EVENTTARGET': 'ddlXN',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': self.__VIEWSTATE_info_course_schedule,
            'ddlXN': xn,
            'ddlXQ': xq,
        }
        url2 = self.baseUrl + "/xsxkqk.aspx?xh=" + self.st_num + "&xm=" + self.st_urlName + "&gnmkdm=N121615"
        response2 = self.session.post(url2, data = data2)
        ans = response2.content.decode('GBK')
        # print(ans)
        return ans.encode('utf-8')

    def sp_class(self, xn = None,xq = None):
        # 选择学期

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
        return ans.encode('utf-8')