import sqlite3

conn = sqlite3.connect('example.db')

c = conn.cursor()

'''c.execute('CREATE TABLE keywords (keyword text PRIMARY KEY, search_vol int)')
c.execute('CREATE TABLE related_keywords (related_keyword text PRIMARY KEY, search_vol int, keyword text, FOREIGN KEY(keyword) REFERENCES keywords(keyword))')'''

#c.execute("DELETE FROM keywords WHERE keyword='toxicologist'")
#c.execute("INSERT INTO keywords VALUES ('toxicologist', 500)")
c.execute('SELECT * FROM keywords')
c.execute('SELECT * FROM related_keywords')
print c.fetchall()

'''
import requests
import os.path
import pprint

path = os.path.dirname(os.path.abspath('grepkey.txt'))
filename = 'grepkey.txt'

with open('/Users/Mig/Desktop/grepkey.txt', 'r') as outfile:
	grepkey = outfile.read()


r = requests.get('http://api.grepwords.com/lookup?apikey={0}&q={1}'.format(grepkey, 'psychiatrist'))
data = r.json()

pprint.pprint(data)

print data[0]['gms']

r = requests.get('http://api.grepwords.com/related?apikey={0}&q={1}'.format(grepkey, 'psychiatrist'))
data = r.json()

pprint.pprint(data)
'''

'''from fuzzywuzzy import fuzz
from fuzzywuzzy import process

foo = 'hematologist'
bar = 'hematologist/oncologist'


print fuzz.ratio(foo, bar)

print fuzz.partial_ratio(foo, bar)

print fuzz.token_sort_ratio(foo, bar)

print fuzz.token_set_ratio(foo, bar)'''

