#! /usr/bin/env python

from __future__ import print_function

import csv
import sys
from collections import Counter, OrderedDict

def main(table):
	with open(table, 'rU') as table_f:
		rdr = csv.DictReader(table_f, delimiter='\t', dialect='excel')
		summary = OrderedDict()
		data = list(rdr)
		for name in rdr.fieldnames[1:]:
			summary[name] = Counter([r[name] for r in data])
		total = len(data)
		print("Summary:")
		for name, results in summary.items():
			print('{}:'.format(name))
			for result, num in results.items():
				if result:
					print("\t - {}: {} of {}".format(result, num, total))

		

if __name__ == '__main__':
	main(sys.argv[1])