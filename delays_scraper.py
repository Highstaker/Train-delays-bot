#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup as bs
import re

# class TrainDelayScraper:
# 	"""docstring for TrainDelayScraper"""
# 	def __init__(self):
# 		super(TrainDelayScraper, self).__init__()

	# @staticmethod
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
		# print("content", content)#debug

		# print(soup.findAll(name="table", id="GridViewETNS_N"))#debug

		def filter_row(row):

			# print("row",row.findAll(name="td"))#debug

			# 0 - train number, 1 - asterik, if present, te trin is AT the station, 2 - station name
			# 3 - B stoplight, asterisks, delay
			row_parse = [i.text.strip(" \n\r\t").replace(u"\xa0", " ") for i in row.findAll(name="td")]
			
			# print("row_parse",row_parse)#debug
			# text = row.text.strip(" \n\r\t").replace(u"\xa0", " ")

			# #add missing space before the delay number
			# plus_index = text.rfind('+')
			# minus_index = text.rfind('-')
			# if plus_index != -1:
			# 	text = text[:plus_index] + " " + text[plus_index:]
			# elif minus_index != -1:
			# 	text = text[:minus_index] + " " + text[minus_index:]

			# # remove empty strings
			# parse = list(filter(bool, text.split(" ")))


			# text = text.replace(" ","")
			# print(text)#debug

			# parse = list(re.findall(r"(^[0-9]+[A-Za-z]?)(\*?)([^\*]*)(\**)(B?)(\+[0-9]+|-[0-9]+)$", text))

			try:
				# parse = [i.strip(" \n\t\r") for i in parse[0]]

				delay_parse = list(re.findall(r"(\**)(B?)(\+[0-9]+|-[0-9]+)$", row_parse[3].strip(" \n\t\r").replace(" ","")))[0]
				# print("delay_parse",delay_parse)#debug
				
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

	else:
		result = None

	return result

if __name__ == '__main__':
	print(get_data())