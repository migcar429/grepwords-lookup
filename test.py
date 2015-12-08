'''import sqlite3

conn = sqlite3.connect('example.db')

c = conn.cursor()'''
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

from fuzzywuzzy import fuzz
from fuzzywuzzy import process

foo = 'toxicologist'
bar = 'copperheaist'


print fuzz.ratio(foo, bar)

print fuzz.partial_ratio(foo, bar)

print fuzz.token_sort_ratio(foo, bar)

print fuzz.token_set_ratio(foo, bar)

