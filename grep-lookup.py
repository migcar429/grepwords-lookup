import pprint
import json
import requests
import os.path
from xlwings import Workbook, Range
from fuzzywuzzy import fuzz, process
import argparse

# Parse 1 terminal argument - file containing keywords. 
'''parser = argparse.ArgumentParser()
parser.add_argument('keywords_file', help='Input the full name of the file, including the extension. E.g. keywords.xlsx')

args = parser.parse_args()
real_keywords_list = args.keywords_file'''

# Read API key from .txt file. 
f = open('/Users/Mig/Desktop/grepkey.txt', 'r') 
grepkey = f.read()
f.close()

# File name of .xlsx or .csv with keywords and range on sheet.
keywords_list = 'specialtykeywords.xlsx'
keywords_range = 'B2'

# Target output file.
txt_file = 'data.txt'

# Set this to the minimum search volume that the client cares about.
search_vol_threshold = 1000

# Exclude related keywords containing these strings:
#taboo_words = ['salary', 'what is', 'what does', 'definition', 'program', 'programs', 'how to', 'porn', 'jobs', 'job', 'become']
taboo_words = ['salary']

def read_specialties(filename):
	# Open workbook, take the list of specialty values.
	path = os.path.dirname(os.path.abspath(__file__))
	wb = Workbook(path + '/' + filename)
	
	# Remove duplicates.
	specialties = list(set(Range(keywords_range).vertical.value))

	return specialties

def lookup_volume(specialties):
	# Data = list of tuples to enable usage of Cursor.executemany()
	search_vol_data = []
	for specialty in specialties:
		r = requests.get('http://api.grepwords.com/lookup?apikey={0}&q={1}'.format(grepkey, specialty))
		r = r.json()

		# Placeholder to break at 10 queries (for testing).
		if specialty == specialties[5]:
			global foo
			foo = search_vol_data
			break

		# ==1 condition is because API returns {error:error_info} for no search data.
		if len(r[0]) == 1:
			search_vol_data.append((specialty, 0))
		else:
			# r[0] because API returns a 1 element list.
			search_vol_data.append((specialty, r[0]['gms']))

	pprint.pprint(search_vol_data)
	print len(search_vol_data)
	return search_vol_data


def lookup_related(specialties):
	related_vol_data = []

	#related_words_pre = ['nearest', 'child', 'find', 'find a', 'medicare', 'medicaid']

	#related_words_suff = ['s near me', 'near me', 'clinic', 'clinic near me', 'locations']
	
	# For testing: check all returned from 'related' query.
	'''for specialty in specialties:
		r = requests.get('http://api.grepwords.com/related?apikey={0}&q={1}&results={2}'.format(grepkey, specialty, 10))
		r = r.json()
		for kw in r:
			print kw['keyword'], '   ', kw['gms']'''

	# For each specialty, query related keywords via API and then append tuples of values to a list.
	for specialty in specialties:
		r = requests.get('http://api.grepwords.com/related?apikey={0}&q={1}&results={2}'.format(grepkey, specialty, 2))
		r = r.json()
		for kw in r:
			# API returns the keyword itself as well, this is to exclude that.
			if kw['keyword'].lower() == specialty.lower():
				pass
			# Filter search volume + makes sure that the keyword (all words in search term) is found within the related term.
			elif fuzz.token_set_ratio(kw['keyword'].lower(), specialty.lower()) == 100 and kw['gms'] >= search_vol_threshold:
				# Checks taboo_words in related keywords, breaks out of loop the moment a taboo_word is found.
				for taboo_word in taboo_words:
					if taboo_word in kw['keyword']:
						break
				# When taboo_words is exhausted (i.e. contains no useless strings), continues to append the data.
				else:
					related_vol_data.append((specialty, kw['keyword'], kw['gms']))
					#related_vol_data.update({kw['keyword']:kw['gms']})

	pprint.pprint(related_vol_data)
	print len(related_vol_data)
	return related_vol_data

def write_to_txt(filename, data_list):

	with open(filename, 'a+') as outfile:
		outfile.write('\n'.join('%s, %s' % x for x in data_list[0]))
		outfile.write('\n'.join('%s, %s, %s' % x for x in data_list[1]))

def main():
	
	specialties = read_specialties(keywords_list)
	search_vol_data = lookup_volume(specialties)
	related_vol_data = lookup_related(specialties)
	write_to_txt(txt_file, [search_vol_data, related_vol_data])

if __name__ == '__main__':
	main()