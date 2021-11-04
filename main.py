import json
import re
import hashlib
import datetime


class CountryIterator:
	host = 'https://en.wikipedia.org/wiki'

	def __init__(self, path_open, path_write):
		self.file_open = open(path_open)
		self.file_write = open(path_write, 'w', encoding='utf-8')

	def __iter__(self):
		self.countries_data = json.load(self.file_open)
		return self

	def __next__(self):
		if not self.countries_data:
			self.file_open.close()
			self.file_write.close()
			raise StopIteration
		country = self.countries_data.pop()
		country_name = re.sub(' ', '_', country['name']['common'])
		country_link = f'{self.host}/{country_name}'
		self.country_dict = {country_name: country_link}
		self.file_write.write(f'{country_name}: {country_link}\n')
		return self.country_dict


path_file = 'countries.json'
write_file = 'countries.txt'
log_path = 'log.txt'
countries_list = []
hash_list = []


def logger(path):
	def _logger(old_function):
		def new_function(*args, **kwargs):
			result = old_function(*args, **kwargs)
			with open(path, "a", encoding='utf-8') as log:
				log.write(f'{datetime.datetime.now()}\nВызвана функция {old_function.__name__}\n')
				log.write(f'с аргументами {args} {kwargs}\n')
				log.write(f'возвращён результат {result}\n')
			log.close()
			return result
		return new_function
	return _logger


@logger(log_path)
def hash_gen(path):
	with open(path) as file:
		json_data = json.load(file)
		for string in json_data:
			str_hash = hashlib.md5(json.dumps(string).encode()).hexdigest()
			yield str_hash


@logger(log_path)
def get_countries():
	for country in CountryIterator(path_file, write_file):
		countries_list.append(country)
	return countries_list


@logger(log_path)
def get_hash():
	for str_hash in hash_gen(path_file):
		hash_list.append(str_hash)
	return hash_list

if __name__ == '__main__':
	hash = get_hash()
	countries = get_countries()

