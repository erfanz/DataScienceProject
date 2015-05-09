import sys
import csv
import argparse

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-input', required=True, help='Path to Inst data file')
	parser.add_argument('-output', required=True, help='Path/filename to save output as')
	opts = parser.parse_args()

	output_file = open(opts.output, 'w')
	# csv_writer = csv.writer(output_file)

	# the codes that mean computer science
	output_file.write('{"type":"FeatureCollection","features":[\n')

	with open(opts.input, 'rb') as f:
		for row in f:
			# {"type":"Feature","id":"01","geometry":{"type":"Point","coordinates":[-86.766233,33.001471]},"properties":{"name":"Alabama","population":4447100}},

			# NOTE:  You will need to strip the header row out of the output
			
			row_list = row.split(",")
			unit = row_list[0]
			name = row_list[1]
			addr = row_list[2]
			city = row_list[3]
			state = row_list[4]
			zip_code = row_list[5]
			website = row_list[15]
			price_calc = row_list[19]	
			lng = row_list[64]
			lat = row_list[65]

			return_string = '{"type":"Feature","id":"' + unit + '","geometry":{"type":"Point","coordinates":[' + lng + ',' + lat + ']}, "properties":{"name":' + name + ',"addr":' + addr + ',"city":' + city + ',"state":' + state + ',"zip_code":' + zip_code + ',"website":' + website + ',"price_calc":' + price_calc + '}},\n'
			output_file.write(return_string)

	output_file.write(']}')
	output_file.close()

if __name__ == '__main__':
	main()
