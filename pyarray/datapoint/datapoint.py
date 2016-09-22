from copy import deepcopy
import numpy as np
from ..label.label import Label

class Point(object):
	def __init__(self, data, labels):
		assert type(data).__module__ == np.__name__, \
		'data must be a numpy.ndarray'

		assert isinstance(labels, Label), \
		'labels must be a Label object'

		assert len(data.shape) <= 2, \
		'Data can only have two dimensions'

		self.data = deepcopy(data)
		self.labels = deepcopy(labels)

	def __eq__(self,other):
		if isinstance(other, Point) is False:
			return False
		if self.labels == other.labels is False:
			return False
		return all(self.data == other.data)

	def __contains__(self, item):
		return item in self.labels

	def __getitem__(self, key):
		return self.labels[key]

	def __setitem__(self, key, value):
		self.labels[key] = value

	def keys(self):
		return self.labels.keys()

