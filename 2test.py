import re


eq = '-2x^2-4x-3'
eq = eq.lower()

var = re.findall(r'[a-z]', eq)
if all(x == var[0] for x in var):
    var = var[0]
print(var)


# poly = re.split(r'\-', eq)
# print(poly)

# for x in re.finditer(r'\-', eq):
#     print(x.span())
