class Value: 

    def __init__(self, data, _children=()):
        self.data = data
        # set for unique constraint
        self.children = set(_children)

    def __repr__(self):
        # pretty printing
        return f"Value(data = {self.data})"
    
    def __add__(self, other):
        if isinstance(other, Value):
            return Value(self.data + other.data, (self, other))
        return Value(self.data + other)
    
    def __mul__(self, other):
        if isinstance(other, Value):
            return Value(self.data * other.data, (self, other))
        return Value(self.data * other)