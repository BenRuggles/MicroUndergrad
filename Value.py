class Value: 

    def __init__(self, data, _children=(), op='', label=''):
        self.data = data
        self.grad = 0
        self._backward = lambda: None
        self._prev = set(_children)
        self.op = op
        self.label = label

    def __repr__(self):
        # pretty printing
        return f"Value(data = {self.data})"
    
    def __add__(self, other):
        out = Value(self.data + other.data, (self, other), '+')
        
        def _backward():
            self.grad = 1.0 * out.grad
            other.grad = 1.0 * out.grad
        out._backward = _backward

        return out
    
    def __mul__(self, other):
        out = Value(self.data * other.data, (self, other), '*')

        def _backwward():
            self.grad = other.data * out.grad
            other.grad = self.data * out.grad
        out._backward = _backwward

        return out

    def tanh(self): # hyperbolic tangent activation function

        x = self.data
        t = (2 / (1 + (-2 * x).exp())) - 1
        out = Value(t, (self,), 'tanh')

        def _backward():
            self.grad = (1 - t**2) * out.grad
        out._backward = _backward

        return out