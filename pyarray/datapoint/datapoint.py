import numpy as np
from ..label.label import Label

class Point(object):
	def __init__(self, data, labels):
		assert type(data).__module__ == np.__name__, \
		'data must be a numpy.ndarray'

		assert isinstance(labels, Label), \
		'labels must be a Label object'

		assert len(data.shape) < 2, \
		'Data can only have two dimensions'

		self.data = data
		self.labels = labels

	def __contains__(self, item):
		return item in self.labels
