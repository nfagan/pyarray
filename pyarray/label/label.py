from copy import deepcopy
import collections

class Label(collections.MutableMapping):
	def __init__(self, *args, **kwargs):
		self.labels = dict()
		self.update(dict(*args, **kwargs))

	def __eq__(self,other):
		if isinstance(other, Label) is False:
			return False

		if self.keys() == other.keys() is False:
			return False

		# unnest from list, and return uniques only

		return set(self.unnest()) == set(other.unnest())

	def __contains__(self, other):
		if isinstance(other, Label):
			return self.labels == other.labels

		if isinstance(other, list) is False:
			assert isinstance(other, str), \
			'Input must be a string or array of strings'
			other = [other]

		assert all(isinstance(label, str) for label in other), \
		'Input must be a string or array of strings'

		values = self.unnest()

		found = all(label in values for label in other)

		if not found:
			return False

		assert all(values.count(label) == 1 for label in other) is True, \
		"""Requested term appears in multiple fields --
		indexing with 'in' would be ambiguous. Use Label.only() instead
		"""
		return True

	def __getitem__(self, key):
		assert isinstance(key, str) is True, \
		'Can only lookup string keys'

		key = self.__keytransform__(key)

		assert key in self.keys(), \
		'The requested key ''%s'' is not in the Label object' % key

		return self.labels[key]

	def __setitem__(self, key, value):
		self.labels[self.__keytransform__(key)] = self.ensure_str_list(value)

	def __delitem__(self, key):
		del self.labels[self.__keytransform__(key)]

	def __str__(self):
		return '\n<Label> with keys: ' + ', '.join(self.keys()) + '\n'

	def __iter__(self):
		return iter(self.labels)

	def __len__(self):
		return len(self.labels)

	def __keytransform__(self, key):
		return key.lower()

	def keys(self):
		return self.labels.keys()

	def values(self):
		return self.labels.values()

	def ensure_str_list(self, value):
		if isinstance(value, list):
			assert all(isinstance(val, str) for val in value), \
			'All values in the list must be strings'
		else:
			assert isinstance(value, str), \
			'All values in the list must be strings'
			value = [value]

		# store a list of unique ids only

		return list(set(value))

	def unnest(self):
		return [label for field in self.values() for label in field]

	def iskey(self, key):
		return key in self.keys()

	def findkey(self, value):
		if value not in self:
			return list()

		return [key for key in self.keys() if value in self[key]][0]

	def replace(self, searchfor, repwith):
		assert all([isinstance(searchfor, str), isinstance(repwith, str)]), \
		'<searchfor> and <repwith> must be strings'

		if searchfor not in self:
			return False 	#	we couldn't find the term

		key = self.findkey(searchfor)
		self[key].remove(searchfor)
		self[key].append(repwith)
		self[key] = list(set(self[key]))

		return True		#	we found the term we were looking for








		
