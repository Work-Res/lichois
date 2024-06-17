from abc import ABC, abstractmethod
import json
from decouple import config


class BaseConfigLoader(ABC):
	@abstractmethod
	def load(self):
		pass


class EnvConfigLoader(BaseConfigLoader):
	def load(self):
		process_str = config('MINISTER_APPROVAL_PROCESSES', default="")
		return process_str.split(',')


class JSONConfigLoader(BaseConfigLoader):
	def __init__(self, file_path, key):
		self.file_path = file_path
		self.key = key
	
	def load(self):
		with open(self.file_path, 'r') as file:
			config_data = json.load(file)
		return config_data.get(self.key, [])
