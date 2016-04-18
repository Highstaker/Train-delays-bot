#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
import pickle
import logging
from copy import deepcopy

class SubscribersHandler:
	"""docstring for SubscribersHandler"""

	def __init__(self, savefile_path, initial_params, from_file=True):
		super(SubscribersHandler, self).__init__()
		self.subscribers = dict()
		self.subscribers_backup_filename = savefile_path  # backup filepath
		self.initial_params = initial_params  # a list of parameters to initialize a user with

		if from_file:
			self.loadSubscribers()  # load subscribers from a file, if it exists

	def loadSubscribers(self):
		"""
		Loads subscribers from a file. Show warning if it doesn't exist.
		"""
		try:
			with open(self.subscribers_backup_filename, 'rb') as f:
				self.subscribers = pickle.load(f)
				logging.warning(("self.subscribers", self.subscribers))
		except FileNotFoundError:
			logging.warning("Subscribers backup file not found. Starting with empty list!")

	def saveSubscribers(self):
		"""
		Saves a subscribers list to file
		"""
		with open(self.subscribers_backup_filename, 'wb') as f:
			pickle.dump(self.subscribers, f, pickle.HIGHEST_PROTOCOL)

	def initializeUser(self, chat_id, force=False, params=None, save=True):
		"""
		Initializes a user with initialparams
		:param chat_id: user's chat id number
		:param force: if False, do not initialize a user if they already exist
		:param params: a dictionary of parameters that should be assigned on initialization
		:param save: saves the subscribers list to file if True and if initialization took place
		:return: None
		"""
		if not (chat_id in self.subscribers.keys()) or force:
			# T T = T
			# F T = T
			# T F = T
			# F F = F
			self.subscribers[chat_id] = deepcopy(self.initial_params)
			if params:
				for i in params:
					self.subscribers[chat_id][i] = params[i]
			if save:
				self.saveSubscribers()

	def getEntry(self, chat_id, param):
		"""
		Returns a parameter from subscribers list.
		:param chat_id: user's chat id number
		:param param: a key of a parameter to be retrieved
		:return: a specified parameter
		"""
		return self.subscribers[chat_id][param]

	def setEntry(self, chat_id, param, value, save=True, append=False):
		"""
		Sets the given parameter to a certain value
		:param append: if False, the parameter is set to value. It True, the value is appended to the prarmeter (e.g. list)
		:param chat_id: user's chat id number
		:param param: a key of a parameter to be modified
		:param value: value to set to a parameter
		:param save: saves the subscribers list to file if True
		:return: None
		"""
		if append:
			self.subscribers[chat_id][param] += value
		else:
			self.subscribers[chat_id][param] = value
		if save:
			self.saveSubscribers()

	def pop_from_param(self,chat_id,param,index):
		"""
		Pops a value from a list, if it is a list. Does nothing if it is not.
		:param chat_id: user's chat id number
		:param param: a key of a parameter to be modified
		:param index: index of a value to be removed
		:return: the removed value. None if it was not a list/
		"""
		if isinstance(self.subscribers[chat_id][param],list):
			try:
				val = self.subscribers[chat_id][param].pop(index)
				return val
			except IndexError:
				return None
		else:
			return None