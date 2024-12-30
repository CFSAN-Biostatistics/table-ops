#!/usr/bin/env python3

import csv
import sys


def main(headers):
	rows = csv.DictReader(sys.stdin, delimiter='\t', dialect='excel-tab')

	# More efficient header check using set intersection
	if not set(headers).intersection(rows.fieldnames):
		raise ValueError(f"Couldn't find any of supplied headers ({', '.join(map(repr, headers))}) in the table.")

	# Optimized sorting using tuple comparison (generally faster than list comparison)
	items = sorted(rows, key=lambda d: tuple(d.get(h, "") for h in headers))

	wr = csv.DictWriter(sys.stdout, dialect='excel-tab', fieldnames=rows.fieldnames)
	wr.writeheader()
	wr.writerows(items)
	# sys.stdout.flush()


if __name__ == '__main__':
	main(sys.argv[1:])