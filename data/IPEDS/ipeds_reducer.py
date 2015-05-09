import sys
import csv
import argparse

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-schools', required=True, help='Path to list of schools to keep')
	parser.add_argument('-input', required=True, help='Path to IPEDS data file')
	parser.add_argument('-output', required=True, help='Path/filename to save output as')
	parser.add_argument('-flag', help='Use "c" to process a completion file')
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

	# the codes that mean computer science


	with open(opts.input, 'rb') as f:

		if opts.flag == 'c': #Dealing with a completion file
			for row in f:
				row_list = row.split(",")
				unit = row_list[0]
				cipc = row_list[1].strip('"')
				alevel =  row_list[3]
				if unit == "UNITID": #Keep the header row
					output_file.write(row.rstrip("\n"))
				#if keeping this school, award level = phd and program code is in Comp sci family
				elif unit in school_ID_list and alevel == '17' and cipc[:3] == '11.' :
					output_file.write(row.rstrip("\n"))

		else:
			# reader = csv.reader(f)
			for row in f: #This treats the row as one long string, which works for this, If we start looking for specific fields we'll use the CSV reader
				if row[0:6] in school_ID_list: #ID's always seem to be 6 characters
					output_file.write(row.rstrip("\n"))

	output_file.close()
	# TODO - think about filtering down to just the fields we need, which might require another arguement flag since each file is different

if __name__ == '__main__':
	main()
