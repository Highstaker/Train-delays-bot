#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-

from textual_data import *

def getMainMenu(subscribed):
	"""
	Returns a representation of custom keyboard to be passed to message-sending functions
	:param subscribed: is the user subscribed?
	Affects which button shall be displayed, subscribe or unsubscribe
	:return: list of lists
	"""

	# subscribe_button = [UNSUBSCRIBE_BUTTON, SHOW_PERIOD_BUTTON] if subscribed else [SUBSCRIBE_BUTTON]

	MAIN_MENU_KEY_MARKUP = [
	[GET_FULL_TABLE_BUTTON],
	[GET_USER_TRAINS_LIST_BUTTON, GET_USER_TRAINS_DELAYS_BUTTON],
	[HELP_BUTTON, ABOUT_BUTTON, OTHER_BOTS_BUTTON],
	[EN_LANG_BUTTON, RU_LANG_BUTTON]
	]

	return MAIN_MENU_KEY_MARKUP