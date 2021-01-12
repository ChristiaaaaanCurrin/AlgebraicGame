

class Set:
	def __init__(self, *elements, membership=None):
		self.membership = membership
		self.elements = ()
		[self.add_element(item) for item in elements]

	def __eq__(self, other):
		if self.membership:
			if other.membership:
				return NotImplemented
			else:
				return False
		else:
			return self.elements == other.elements

	def copy(self):
		return Set(*self.elements, membership=self.membership)

	def element(self, item):
		if self.membership:
			return self.membership(item) or item in self.elements
		else:
			return item in self.elements

	def add_element(self, item):
		if not self.element(item):
			self.elements += (item,)


def union(a, *sets):
	a = a.copy
	if a.membership:
		for b in sets:
			if b.membership:
				a.membership = lambda x: a.membership(x) or b.membership(x)
			[a.add_element(x) for x in b.elements]
	else:
		for b in sets:
			if b.membership:
				a.membership = b.membership
			[a.add_element(x) for x in b.elements]


def intersection(a, *sets):
	a = a.copy
	if a.membership:
		for b in sets:
			if b.membership:
				pass


x = Set()
print(x.membership, x.elements)
y = Set(x)
print(y.__dict__)
print(type(()) == tuple)