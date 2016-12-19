
import platform
import os
import re
import requests
from bs4 import BeautifulSoup

tt = "欢迎使用正方教务管理系统"

print(tt.find("请登录") == -1)


st_num = '15999222'  # 学号
password = 'dhn78834'  #
name = '董华楠'  # 姓名
urlName = '%B6%AD%BB%AA%E9%AA'
session = requests.session()
baseUrl = "http://210.30.208.200/"

# 访问教务系统
print("正在尝试登录......")
session.headers[
    'User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
response = session.get(baseUrl)
baseUrl = response.url
baseUrl = re.subn(r'.default2.aspx', '', baseUrl)[0]
loginUrl = baseUrl + '/default2.aspx'
response = session.get(loginUrl)
__VIEWSTATE = re.findall("name=\"__VIEWSTATE\" value=\"(.*?)\"", response.content.decode('GBK'))[0]
# print(__VIEWSTATE)
print("Got viewatate")
print( "正在获取验证码......" )
imgUrl = baseUrl + "/CheckCode.aspx?"
imgresponse = session.get(imgUrl, stream=True)
image = imgresponse.content

# 保存code
if 'Linux' in platform.system():
    DstDir = os.getcwd() + "/"
    print(DstDir)
    with open(DstDir + "code.jpg", "wb") as jpg:
        jpg.write(image)
        print("保存验证码到：" + DstDir + "code.jpg" + "\n")

    os.popen("display " + DstDir + "code.jpg")
else:
    DstDir = os.getcwd() + "\\"
    print(DstDir)
    with open(DstDir + "code.jpg", "wb") as jpg:
        jpg.write(image)
        print("保存验证码到：" + DstDir + "code.jpg" + "\n")

    command = "start" + " \"\" " + DstDir +"code.jpg"
    x = os.popen( command ).read( )
code = input("验证码是：")
RadioButtonList1 = u"学生".encode('gb2312', 'replace')
data = {
    "RadioButtonList1": RadioButtonList1,
    "__VIEWSTATE": __VIEWSTATE,
    "txtUserName": st_num,
    "TextBox2": password,
    "Button1": "",
    "txtSecretCode": code,
}

Loginresponse = session.post(loginUrl, data=data)
if Loginresponse.status_code == requests.codes.ok:
    print("成功进入教务系统！")
# print(Loginresponse.text)

url2 = baseUrl + "/xs_main.aspx?xh=" + st_num
session.headers['Referer'] = baseUrl + "default2.aspx"
response2 = session.get(url2)
html = response2.content.decode("gb2312")
print(html)

soup = BeautifulSoup(html, 'html.parser')
title = soup.title
print(title.get_text())