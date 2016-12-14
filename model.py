import cal
import spider
import show_gpa

if __name__ == "__main__":
	ob = spider.Student()
	ob.login()
	while 1:
		switch = input("输入 1 ：获取课表并转为ical\t 输入 2 ：查询学期成绩\n")
		# print(switch)
		if switch == '1':
			cal.get_cal(ob)
		if switch == '2':
			show_gpa.show_GPA( ob )


