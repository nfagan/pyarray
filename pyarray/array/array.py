from copy import deepcopy
from ..label.label import Label
from ..datapoint.datapoint import Point
from itertools import product
import numpy as np

class Array(object):
	def __init__(self, points):
		assert isinstance(points, list), \
		'points must be a list of Points'

		assert all([isinstance(point, Point) for point in points]), \
		'points must be a list of Points'

		assert all([set(point.keys()) == set(points[0].keys()) for point in points]), \
		'points must have consistent keys'

		self.points = deepcopy(points)

	def __len__(self):
		return len(self.points)

	def __repr__(self):
		return self.__str__()

	def __str__(self):
		uniq = self.uniques()
		rep = ''
		for key in uniq.keys():
			rep = rep + '\n' + key.upper() + ':'
			for value in uniq[key]:
				rep = rep + '\n\t' + value
		return rep

	def __contains__(self, value):
		return any([value in point for point in self.points])

	def find(self, value):
		return [i for i, point in enumerate(self.points) if value in point]

	def only(self, values):
		self.points = [point for point in self.points if values in point]

	def unnest(self, values):
		return [item for sublist in values for item in sublist]

	def __getitem__(self, key):
		if isinstance(key, str):
			return list(set(self.unnest([point[key] for point in self.points])))
		if isinstance(key, int):
			return Array([self.points[key]])
		raise Exception('Unsupported indexing method')

	def __setitem__(self, key, value):
		if isinstance(key, str):
			for point in self.points:
				point[key] = value
			return
		if isinstance(key, int):
			assert isinstance(value, Point), \
			'Must set a Point object with this indexing method'
			self.points[key] = deepcopy(value)
			return

		raise Exception('Unsupported indexing / setting method')

	def keys(self):
		if len(self):
			return self.points[0].keys()
		return []

	def replace(self, searchfor, repwith):
		[point.labels.replace(searchfor, repwith) for point in self.points]

	def uniques(self):
		uniqs = {}
		for key in self.keys():
			uniqs[key] = self[key]
		return uniqs

	def getcombs(self, within):
		assert isinstance(within, list), 'within must be a list of strings'
		assert all([isinstance(item, str) for item in within]), \
		'within must be a list of strings'

		labels = [self[key] for key in within]
		return list(product(*labels))

	def getindices(self, within):
		combs = self.getcombs(within)
		return [self.find(list(comb)) for comb in combs if len(self.find(list(comb))) > 0]

	def index(self, indices):
		assert isinstance(indices, list), 'indices must be a list'
		return Array([self.points[i] for i in indices])

	def getdata(self):
		arrays = [point.data for point in self.points]
		return np.concatenate(arrays,axis=0)




