#!/usr/bin/env python3

import csv
import sys

def main(headers):
	rows = csv.DictReader(sys.stdin, delimiter='\t', dialect='excel-tab')
	if not any([str(header) in rows.fieldnames for header in headers]):
		raise ValueError("Couldn't find any of supplied headers ({}) in the table.".format(','.join(['"{}"'.format(header) for header in headers])))
	items = list(rows)
	items.sort(key=lambda d: [d.get(h) or "" for h in headers])
	wr = csv.DictWriter(sys.stdout, dialect='excel-tab', fieldnames=rows.fieldnames)
	wr.writeheader()
	wr.writerows(items)
	sys.stdout.flush()

if __name__ == '__main__':
	main(sys.argv[1:])