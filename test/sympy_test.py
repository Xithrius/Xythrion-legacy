import sympy as sp
sp.init_printing()

"""
x, y, z = sympy.symbols('xyz')
p = sympy.Plot(x * y ** 3 - y * x ** 3)
p.saveimage(path('plot.png'), format='png')
sp.integrate(f, x)
expr = sympy.sin(sympy.sqrt(sympy.symbols('x')**2 + 20)) + 1
"""

x, y, z = sp.symbols('x y z')
# f = sp.sin(x * y) + sp.cos(y * z)
f = x * y ** 3 - y * x ** 3
sp.preview(f, viewer='file', output='png', filename=path('output.png'))
