#! /usr/bin/env python
import csv
import sys



def main(unionize=True, *files):
	header = []
	items = []
	possible_identity_headers = None
	for fi in files:
		with open(fi, 'rU') as table:
			reader = csv.DictReader(table, delimiter='\t', dialect='excel-tab')
			rows = list(reader)
			for field in reader.fieldnames:
				if field not in set(header):
					header.append(field)
				
					
				#try to find identity columns in the files, to use to join
				if possible_identity_headers is None:
					possible_identity_headers = set(reader.fieldnames)
				#winnow down the shared columns in each file by whether they're present in all, and all their values are unique in each file and not null
				#because these are the most likely to be shared keys
				possible_identity_headers = possible_identity_headers.intersection(filter(lambda f: len(set([r[f] for r in rows])) == len(rows) and all([r[f] is not None for r in rows]), reader.fieldnames))
			items.extend(rows)
	
	# if len(possible_identity_headers) > 1:
	# 	#if there's more than one, we need to check that joining on any one of them produces the same results

	# 	#finally
	# 	possible_identity_headers = set((possible_identity_headers.pop(), ))

	#if we found an identity column, then try to join rows
	if possible_identity_headers and unionize:
		key_column = possible_identity_headers.pop()
		keys = set([r[key_column] for r in items])
		merged_rows = []
		for key in sorted(keys):
			new_row = {}
			for row in filter(lambda r: r[key_column] == key, items):
				new_row.update(row)
			merged_rows.append(new_row)
		items = merged_rows

	wr = csv.DictWriter(sys.stdout, delimiter='\t', dialect='excel-tab', fieldnames=header)
	wr.writeheader()
	wr.writerows(items)


if __name__ == '__main__':
	main(*sys.argv[1:])