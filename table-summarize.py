#! /usr/bin/env python

from __future__ import print_function

import csv
import sys
from collections import Counter, OrderedDict


def main(table):
	with open(table, 'r', newline='', encoding='utf-8') as table_f:  # Improved file opening
		rdr = csv.DictReader(table_f, delimiter='\t', dialect='excel')

		# Check if fieldnames exist before proceeding to avoid potential errors
		if not rdr.fieldnames or len(rdr.fieldnames) <= 1:
			print("No data columns found in the table.")
			return

		summary = OrderedDict()
		for row in rdr:  # Iterate directly without creating a list in memory
			for name in rdr.fieldnames[1:]:
				summary.setdefault(name, Counter()).update([row[name]])  # More efficient counting

		total = rdr.line_num - 1  # get the number of rows

		print("Summary:")
		for name, results in summary.items():
			print(f'{name}:')  # f-string
			for result, num in results.items():
				if result:
					print(f"\t - {result}: {num} of {total}")  # f-string


if __name__ == '__main__':
	main(sys.argv[1])