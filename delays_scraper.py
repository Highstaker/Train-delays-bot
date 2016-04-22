#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup as bs
import re

from traceback_printer import full_traceback


def get_data():
	url = "http://kompis.stockholmstag.se/wwwetns/etnsmobil.aspx"

	try:
		req = requests.get(url)
	except requests.exceptions.RequestException:
		return None

	result = []

	if req.ok:

		content = req.content
		soup = bs(content, "html.parser")

		def filter_row(row):

			# 0 - train number, 1 - asterik, if present, te trin is AT the station, 2 - station name
			# 3 - B stoplight, asterisks, delay
			row_parse = [i.text.strip(" \n\r\t").replace(u"\xa0", " ") for i in row.findAll(name="td")]
			
			try:
				# parse = [i.strip(" \n\t\r") for i in parse[0]]

				delay_parse = list(re.findall(r"(\**)(B?)(\+[0-9]+|-[0-9]+)$", row_parse[3].strip(" \n\t\r").replace(" ","")))[0]
				
				parse_dict = dict(number=row_parse[0].strip(" \n\t\r"),
				  departed=not bool(row_parse[1].strip(" \n\t\r")),
				  station=row_parse[2].strip(" \n\t\r"),
				  red_light=bool(delay_parse[1]),
				  delay=delay_parse[2]
				  )

			except IndexError:
				print(full_traceback())
				return

			# print("Verified: ", len(parse)==6 )#debug

			result.append(parse_dict)

		table = soup.findAll(name="table", id="GridViewETNS_N")[0]
		for row in table.findAll(name="tr"):
			filter_row(row)

		table = soup.findAll(name="table", id="GridViewETNS_S")[0]
		for row in table.findAll(name="tr"):
			filter_row(row)

		#extracting time
		cur_time = soup.findAll(name="span",id='LabelTime')[0]
		for br in cur_time.findAll("br"):
			br.replace_with("\n")
		cur_time = cur_time.text.split("\n")[0]

		print(cur_time)#debug

		result = {"time": cur_time, "trains": result}

	else:
		result = None

	return result

if __name__ == '__main__':
	print(get_data())