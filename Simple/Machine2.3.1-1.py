# # -* - coding: UTF-8 -* -
#http://www.ituring.com.cn/article/177439
## Virtual Machine 2.3.1
## 小步语义 -- 表达式
## python 3.4
import functools
import re
_PREFIX = ''
def trace(fn):
    """A decorator that prints a function's name, its arguments, and its return
    values each time the function is called. For example,

    @trace
    def compute_something(x, y):
        # function body
    """
    @functools.wraps(fn)
    def wrapped(*args, **kwds):
        global _PREFIX
        reprs = [repr(e) for e in args] 
        reprs += [repr(k) + '=' + repr(v) for k, v in kwds.items()]
        print('{0}({1})'.format(fn.__name__, ', '.join(reprs)) + ':')
        _PREFIX += '    '
        try:
            result = fn(*args, **kwds)
            _PREFIX = _PREFIX[:-4]
        except Exception as e:
            print(fn.__name__ + ' exited via exception')
            _PREFIX = _PREFIX[:-4]
            raise
        # Here, print out the return value.
        print('{0}({1}) -> {2}'.format(fn.__name__, ', '.join(reprs), result))
        return result
    return wrapped

    

    
class Hex(object):
    """ 数值符号类
    """
    def __init__(self, value):
        self.value = int('0x'+str(value),16)

    def reducible(self):
        return False

    def __repr__(self):
        return '«'+ str(self.value) +'»'     
        
    def __str__ (self):
        return str(self.value.__str__())

class Number(object):
    """ 数值符号类
    """
    def __init__(self, value):
        self.value = value

    def reducible(self):
        return False

    def __repr__(self):
        return '«'+ str(self.value) +'»'     
        
    def __str__ (self):
        return str(self.value.__str__())


class Boolean(object):
    """ 布尔值符号类型
    """
    def __init__(self, value):
        self.value = value

    def reducible(self):
        return False

    def __repr__(self):
        return '«'+ str(self) +'»'         
        
    def __str__ (self):
        #print('__str__  called')
        return 'true' if (self.value) else 'false'



class Add(object):
    """ 加法符号类
    """
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def reducible(self):
        return True

    def reduce(self, environment):
        if self.left.reducible():
            return Add(self.left.reduce(environment), self.right)
        elif self.right.reducible():
            return Add(self.left, self.right.reduce(environment))
        else:
            return Number(self.left.value + self.right.value)

    def __str__ (self):
        return self.left.__str__ () + ' + ' + self.right.__str__ ()
    
    def __repr__(self):
        return '«'+ str(self) +'»'      

class Multiply(object):
    """ 乘法符号类
    """
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def reducible(self):
        return True
        
    @trace
    def reduce(self, environment):
        if self.left.reducible():
            return Multiply(self.left.reduce(environment), self.right)
        elif self.right.reducible():
            return Multiply(self.left, self.right.reduce(environment))
        else:
            return Number(self.left.value * self.right.value)
        
    def __str__ (self):
        return self.left.__str__ () + ' * ' + self.right.__str__ ()

    def __repr__(self):
        return '«'+ str(self) +'»'         

class LessThan(object):
    """ 小于符号类
    """
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def reducible(self):
        return True

    def reduce(self, environment):
        if self.left.reducible():
            return LessThan(self.left.reduce(environment), self.right)
        elif self.right.reducible():
            return LessThan(self.left, self.right.reduce(environment))
        else:
            return Boolean(self.left.value < self.right.value)

    def __repr__(self):
        #print('__repr__ called')
        return '«'+ str(self) +'»' 
            
            
    def __str__ (self):
        #print('__str__  called')
        return str(self.left) + ' < ' + self.right.__str__ ()


class Variable(object):
    """ 变量符号类
    """
    def __init__(self, name):
        self.name = name

    def reducible(self):
        return True

    def reduce(self, environment):
        return environment[self.name]

    def __str__ (self):
        return str(self.name)


class Machine(object):
    """ 虚拟机
    """
    def __init__(self, expression, environment):
        self.expression = expression
        self.environment = environment

    def step(self):
        self.expression = self.expression.reduce(self.environment)

    def run(self):
        while self.expression.reducible():
            print(str(self.expression))
            self.step()
        print(self.expression)
        return -1# return = return None = no statement
            

## test
## 在虚拟机中运行表达式

##1 * 2 + 3 * 4 = 14
Machine(Add(Multiply(Number(1), Number(2)),
            Multiply(Number(3), Number(4))),
        {}
        ).run()

print('')

##5 < 2 + 2
Machine(
    LessThan(Number(5), Add(Number(2), Number(2))),
    {}
    ).run()

print('')


##x = 3; y = 4; x + y = 7
Machine(
    Add(Variable('x'), Variable('y')),
    {'x':Number(3), 'y':Number(4)}
    ).run()

LessThan(Number(5), Add(Number(2), Number(2)))
expression  = Number(5)
expression  = Add(Number(2), Number(2))
expression  = Multiply(Number(2), Number(2))
expression  = LessThan(Number(5), Add(Number(2), Number(2)))
e  = LessThan(Multiply(Number(2), Variable('x')), Add(Number(3), Number(4)))
e.reduce({'x': Number(3)})
#e.evaluate({'x': Number(3)})
print('');print('')
Machine(
   LessThan(Multiply(Number(2), Variable('x')), Add(Number(3), Number(4))),
   {'x': Number(3)}
    ).run()
Machine(
   LessThan(Multiply(Hex('B'), Variable('x')), Add(Number(3), Number(4))),
   {'x': Number(3)}
    ).run()
#expression.reduce({x: Number(3)})

