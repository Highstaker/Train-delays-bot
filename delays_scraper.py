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
			text = row.text.strip(" \n\r\t").replace(u"\xa0", " ")

			# #add missing space before the delay number
			# plus_index = text.rfind('+')
			# minus_index = text.rfind('-')
			# if plus_index != -1:
			# 	text = text[:plus_index] + " " + text[plus_index:]
			# elif minus_index != -1:
			# 	text = text[:minus_index] + " " + text[minus_index:]

			# # remove empty strings
			# parse = list(filter(bool, text.split(" ")))

			# print(text)#debug

			parse = list(re.findall(r"(^[0-9]+[A-Za-z]?)(.*)(\+[0-9]+|-[0-9]+)$", text))

			try:
				parse = [i.strip(" \n\t\r*") for i in parse[0]]
			except IndexError:
				return

			# print("Verified: ", len(parse)==3 )#debug

			result.append(parse)

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