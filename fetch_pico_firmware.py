#!/usr/bin/env python3
""" Raspberry Pi Pico Micropython firmware download """

#
# Martin Levy - https://github.com/mahtin/
#

import os
import sys
import re
import time
import getopt
import datetime
import requests
from bs4 import BeautifulSoup

#
# https://micropython.org/download/rp2-pico/
#

BASEURL = 'https://micropython.org'
PATH = '/download/rp2-pico/'

#
# Firmware filenames have the form of rp2-pico-YYYYMMDD-*.rp2
# We use this to both pattern match for the files and also to date/timestamp them
# As there is no time, we use 00:00:00 and also UTC (because that's the right thing to do)
#

verbose_flag = False
overwrite_flag = False
utc_flag = False

extract_date = re.compile("rp2-pico-([0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9])-.*.uf2")

def process_body(body):
	""" Raspberry Pi Pico Micropython firmware download """

	list_of_firmware_files = {}

	for ul in body.find_all('ul'):
		for li in ul.findAll("li", recursive=False):
			for c in li.findAll("a", recursive=False):
				if 'rp2-pico-' in c.get_text():
					firmware = c.get_text().strip()
					path = c['href']
					list_of_firmware_files[path] = firmware
					continue

	return list_of_firmware_files

def find_firmware(url_or_filename):
	""" Raspberry Pi Pico Micropython firmware download """

	if 'http' in url_or_filename:
		response = requests.get(url_or_filename)
		soup = BeautifulSoup(response.text, 'html.parser')
	else:
		soup = BeautifulSoup(open(url_or_filename), 'html.parser')

	return process_body(soup.body)

def touch_file(filename, date):
	""" Raspberry Pi Pico Micropython firmware download """

	global utc_flag

	if utc_flag:
		tzinfo = datetime.timezone.utc
	else:
		tzinfo = None
	d = datetime.datetime(int(date[0:4]), int(date[4:6]), int(date[6:8]), 0, 0, 0, tzinfo=tzinfo)
	t = time.mktime(d.timetuple())
	try:
		os.utime(filename, (t, t))
		if verbose_flag:
			print("%s: touch %s/%d" % (filename, date, t), file=sys.stderr)
	except Exception as e:
		print("%s: %s" % (filename, e), file=sys.stderr)


def download_firmware(filename, full_path_url):
	""" Raspberry Pi Pico Micropython firmware download """

	global overwrite_flag

	if not overwrite_flag:
		if os.path.isfile(filename):
			print("%s: already downloaded, hence skipped" % (filename), file=sys.stderr)
			return

	print("%s: downloading from %s" % (filename, full_path_url), file=sys.stderr)
	try:
		r = requests.get(full_path_url, allow_redirects=True)
		r.raise_for_status()
	except Exception as e:
		print("%s: %s" % (full_path_url, e), file=sys.stderr)
		return

	try:
		with open(filename, 'wb') as fd:
			fd.write(r.content)
	except Exception as e:
		print("%s: %s" % (filename, e), file=sys.stderr)
		return

	try:
		m = extract_date.search(filename)
		date = m.group(1)
		touch_file(filename, date)
	except:
		print("%s: unknown date format in filename", file=sys.stderr)

def download_all_firmware(list_of_firmware_files):
	""" Raspberry Pi Pico Micropython firmware download """

	for path in list_of_firmware_files:
		filename = list_of_firmware_files[path]
		full_path_url = BASEURL + path
		download_firmware(filename, full_path_url)

def doit(args=None):
	""" Raspberry Pi Pico Micropython firmware download """

	global verbose_flag, overwrite_flag, utc_flag

	usage = ('usage: fetch_firmware_rp2 '
		 + '[-H|--help] '
		 + '[-v|--verbose] '
		 + '[-o|--overwrite] '
		 + '[-u|--utc] '
		 )

	try:
		opts, args = getopt.getopt(args,
					   'Hvou',
					   [
					   	'help',
					   	'version',
						'overwrite',
						'utc'
					   ])
	except getopt.GetoptError:
		sys.exit(usage)

	for opt, arg in opts:
		if opt in ('-H', '--help'):
			exit(usage)
		elif opt in ('-v', '--verbose'):
			verbose_flag = True
		elif opt in ('-o', '--overwrite'):
			overwrite_flag = True
		elif opt in ('-u', '--utc'):
			utc_flag = True

	if len(args) > 1:
		sys.exit(usage)

	try:
		url_or_filename = args[0]
	except IndexError:
		url_or_filename = BASEURL + PATH
	r = find_firmware(url_or_filename)
	download_all_firmware(r)
	sys.exit(0)

def main(args=None):
	""" Raspberry Pi Pico Micropython firmware download """

	if args is None:
		args = sys.argv[1:]
	doit(args)

if __name__ == '__main__':
	main()
