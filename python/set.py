

class Set:
	def __init__(self, *elements, membership=None):
		self.elements = []
		[self.add_element(item) for item in elements]
		self.membership = membership

	def copy(self):
		return Set(*self.elements, membership = self.membership)

	def element(self, item):
		if self.membership:
			return self.memebership(item) or item in self.elements
		else:
			return item in self.elements

	def add_element(self, item):
		if not self.element(item):
			self.elements.append(item)

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
			if b.membership
