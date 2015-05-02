import sys
import csv
import argparse

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-schools', required=True, help='Path to list of schools to keep')
	parser.add_argument('-input', required=True, help='Path to IPEDS data file')
	parser.add_argument('-output', required=True, help='Path/filename to save output as')
	opts = parser.parse_args()
	
	# Every IPEDS file starts with the UNITID
	# Our schools list should be just UNITID and a name
	# Load the ID's into a list
	school_ID_list = []
	with open(opts.schools, 'rb') as f:
		reader = csv.reader(f)
		# NOTE:  This keeps the header, which works for us because we then get the first row from the input file which are field names
		for row in reader:
			school_ID_list.append(row[0])

	# open the input file and iterate through it keeps rows where input[0] is in school_ID_list
	# and write that row out to the output file retaining all fields

	output_file = open(opts.output, 'w')
	# csv_writer = csv.writer(output_file)


	with open(opts.input, 'rb') as f:
		reader = csv.reader(f)
		for row in f:
			if row[0:6] in school_ID_list:
				output_file.write(row.rstrip("\n"))

	output_file.close()
	# TODO - think about filtering down to just the fields we need, which might require another arguement flag since each file is different

if __name__ == '__main__':
	main()
