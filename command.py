

import argparse

# 需求分析
# 1. run参数使查询程序运行
# 2. sync同步ZF教务的数据到本地和数据库（如果允许）
# 3. sync2db同步数据到数据库（db）
# 4. synu2local把远程数据库的数据同步到本地（local）


parser = argparse.ArgumentParser()

# 同步数据
# zf_web和db同步到本地 默认web_zf
parser.add_argument('-s', '--sync', dest = 'sync', default='web',nargs = '?',type=str, choices = ['web','database'])
#parser.parse_args(''.split())
# parser.add_argument('-u',nargs='?',default='d')
# 进入查询程序
parser.add_argument('-r', '--run', dest = 'run', default='True', nargs = '?',type = bool)
parser.parse_args(''.split())
# parser.add_argument('-y', '--year', action='store', dest='year',help='choice the academic year you want')
# parser.add_argument('-t', '--term', action='store', dest='term',choices=('1', '2','3','4'),help='choice the term you want')
# parser.add_argument('-o', action='store', dest='output', help='output the icalander file,and the default file is name \'output.ics\'')
parser.add_argument('--version', action='version', version='1.0')
# parser.add_argument('-r', '--interact', action='store_true', default=False, dest='interaction',help='Set mode,if you want to access the script as interaction')

# parser.add_argument('--update',  dest = '', help = 'Update all your informations.')
# parser.add_argument('-s', '--courses', dest = '')
# parser.add_argument('-g', '--grades', dest = '')


# import argparse  
  
# #### 参数调用说明  
# parser = argparse.ArgumentParser()  
# parser.add_argument('-t','--tcp', help='tcp service',action='store_true')  
# parser.add_argument('-u', '--udp', help='udp service', action='store_true')  
# parser.add_argument('-s', '--scheduler', help='one of rr|wrr|lc|wlc|lblc|lblcr|dh|sh|sed|nq,the default scheduler is wlc')  
# parser.add_argument('-p', '--persistent', help='persistent service, default:1500', type = int)  
# parser.add_argument('-r', '--realserver', help="server-address is host (and port) Example: -r '1.1.1.1 2.2.2.2 3.3.3.3'", type = str )  
# parser.add_argument('-f', '--floapingip', help='vip address of lvs' )  
# parser.add_argument('-g', '--gatewaying', help='gatewaying (direct routing)',action='store_true')  
# parser.add_argument('-m','--masquerading', help='masquerading (NAT)', action='store_true')  
# parser.add_argument('-S','--srcport', help='listen on floapip port', type = int )  
# parser.add_argument('-R','--destport', help='listen on realserver port', type = int )  
# args = parser.parse_args() 

print( parser.parse_args())

results = parser.parse_args()
if (results.sync):
    print (results)
