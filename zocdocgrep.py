import pprint
import json
import requests
import os.path
from xlwings import Workbook, Range
from fuzzwuzzy import fuzz, process

# Read API key from .txt file. 
f = open('/Users/Mig/Desktop/grepkey.txt', 'r') 
grepkey = f.read()
f.close()

search_vol_threshold = 2000



def readspecialties(filename):
	# Open workbook, take the list of specialty values.
	path = os.path.dirname(os.path.abspath(__file__))
	wb = Workbook(path + '/' + filename)
	
	specialties = list(set(Range('B2').vertical.value))

	return specialties

def lookupvolume(specialties):
	search_vol_data = {}
	for specialty in specialties:
		r = requests.get('http://api.grepwords.com/lookup?apikey={0}&q={1}'.format(grepkey, specialty))
		r = r.json()

		# Placeholder to break at 10 queries (for testing).
		if specialty == specialties[10]:
			global foo
			foo = search_vol_data
			break

		if len(r[0]) == 1:
			search_vol_data.update({specialty:0})
		else:
			search_vol_data.update({specialty:r[0]['gms']})

	pprint.pprint(search_vol_data)

	return search_vol_data


def lookuprelated(specialties):
	related_vol_data = {}

	#related_words_pre = ['nearest', 'child', 'find', 'find a', 'medicare', 'medicaid']

	#related_words_suff = ['s near me', 'near me', 'clinic', 'clinic near me', 'locations']
	
	for specialty in specialties:
		r = requests.get('http://api.grepwords.com/related?apikey={0}&q={1}&results={2}'.format(grepkey, specialty, 10))
		r = r.json()
		for kw in r:
			if kw['keyword'].lower() == specialty.lower():
				pass
			# Filter search volume + makes sure that the keyword (all words in search term) is found within the related term.
			elif fuzzy.token_set_ratio(kw['keyword'].lower(), specialty.lower()) == 100 and kw['gms'] > search_vol_threshold:
				related_vol_data.update({kw['keyword']:kw['gms']})


	pprint.pprint(related_vol_data)
	return related_vol_data

'''
r = requests.get('http://api.grepwords.com/related?apikey={0}&q={1}'.format(grepkey, 'urgent care'))
data = r.json()

pprint.pprint(data)
'''


def main():
	
	specialties = readspecialties('specialtykeywords.xlsx')
	lookupvolume(specialties)
	lookuprelated(foo)

if __name__ == '__main__':
	main()