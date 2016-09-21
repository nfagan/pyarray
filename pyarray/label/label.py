import collections

class Label(collections.MutableMapping):
	def __init__(self, *args, **kwargs):
		self.labels = dict()
		self.update(dict(*args, **kwargs))

	def __eq__(self, other):
		if isinstance(other, Label):
			return self.labels == other.labels

		if isinstance(other, list) is False:
			assert isinstance(other, str), \
			'Input must be a string or array of strings'
			other = [other]

		assert all(isinstance(label, str) for label in other), \
		'Input must be a string or array of strings'

		values = [label for field in self.values() for label in field]

		found = all(label in values for label in other)

		if not found:
			return False

		assert all(values.count(label) == 1 for label in other) is True, \
		"""Requested term appears in multiple fields --
		indexing with '==' would be ambiguous
		"""
		return True

	def __contains__(self, item):
		values = [label for field in self.values() for label in field]
		return item in values

	def __getitem__(self, key):
		return self.labels[self.__keytransform__(key)]

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

		return value

	def iskey(self, key):
		return key in self.keys()

		
