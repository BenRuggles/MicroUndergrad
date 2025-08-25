import math

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
        other = other if isinstance(other, Value) else Value(other) 
        out = Value(self.data + other.data, (self, other), '+')
        
        def _backward():
            self.grad += out.grad
            other.grad += out.grad
        out._backward = _backward

        return out
    
    def __mul__(self, other):
        other = other if isinstance(other, Value) else Value(other) 
        out = Value(self.data * other.data, (self, other), '*')

        def _backwward():
            self.grad += other.data * out.grad
            other.grad += self.data * out.grad
        out._backward = _backwward

        return out

    def __rmul__(self, other): # other * self
        return self * other
    
    def exp(self): # exponential function
        x = self.data
        t = Value(math.exp(x), (self,), 'exp')
        out = Value(t, (self,), 'tanh')

        def _backward():
            self.grad += out.data * out.grad    
        out._backward = _backward

        return out
    
    def __truediv__(self, other): # self / other
        other = other if isinstance(other, Value) else Value(other)
        return self * other**-1
    
    def __pow__(self, other): # self ** other
        assert isinstance(other, (int, float)), "only supporting int/float powers for now"
        out = Value(self.data**other, (self,), f'**{other}')

        def _backward():
            self.grad += (other * self.data**(other - 1)) * out.grad
        out._backward = _backward

        return out
    
    def tanh(self): # hyperbolic tangent activation function
        x = self.data
        t = (2 / (1 + (-2 * x).exp())) - 1
        out = Value(t, (self,), 'tanh')

        def _backward():
            self.grad = (1 - t**2) * out.grad
        out._backward = _backward

        return out
    
    def backward(self):
        # topological order all of the children in the graph
        topo = []
        visited = set()
        def build_topo(v):
            if v not in visited:
                visited.add(v)
                for child in v._prev:
                    build_topo(child)
                topo.append(v)
        build_topo(self)

        self.grad = 1.0
        for node in reversed(topo):
            node._backward() 