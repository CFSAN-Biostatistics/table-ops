#! /usr/bin/env python
import csv
import sys
from collections import defaultdict


def main(unionize=True, *files):
	header = []
	items = []
	possible_identity_headers = None

	for fi in files:
		with open(fi, 'r', newline='', encoding='utf-8') as table:  # Improved file opening
			reader = csv.DictReader(table, delimiter='\t', dialect='excel-tab')

			# Efficient header update using set operations
			header_set = set(header)
			new_headers = [field for field in reader.fieldnames if field not in header_set]
			header.extend(new_headers)

			rows = list(reader)  # Keep this for now, but see optimization below
			if not rows:  # skip empty files
				continue

			# More efficient identity header detection
			if possible_identity_headers is None:
				possible_identity_headers = set(reader.fieldnames)

			# Optimized identity header filtering
			possible_identity_headers.intersection_update(
				f for f in reader.fieldnames
				if
				len({row[f] for row in rows if f in row}) == len(rows) and all(row.get(f) is not None for row in rows)
			)
			items.extend(rows)

	if possible_identity_headers and unionize:
		key_column = possible_identity_headers.pop()
		# More efficient merging using defaultdict
		merged_rows = defaultdict(dict)
		for row in items:
			key = row.get(key_column)
			if key is not None:  # skip rows with null keys
				merged_rows[key].update(row)
		items = list(merged_rows.values())

	wr = csv.DictWriter(sys.stdout, delimiter='\t', dialect='excel-tab', fieldnames=header)
	wr.writeheader()
	wr.writerows(items)


if __name__ == '__main__':
	main(*sys.argv[1:])