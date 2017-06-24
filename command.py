import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-y', '--year', action='store', dest='year',help='choice the academic year you want')
parser.add_argument('-t', '--term', action='store', dest='term',choices=('1', '2','3','4'),help='choice the term you want')
parser.add_argument('-o', action='store', dest='output', help='output the icalander file,and the default file is name \'output.ics\'')
parser.add_argument('--version', action='version', version='1.0')
parser.add_argument('-r', '--interact', action='store_true', default=False, dest='interaction',help='Set mode,if you want to access the script as interaction')

results = parser.parse_args()