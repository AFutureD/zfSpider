import os
# start "" "D:\code\python\jiaoWu\code.jpg"
command = "start" +" \"\" " + "D:\\code\\python\\jiaoWu\\code.jpg"
x = os.popen(command).read()
print(x)