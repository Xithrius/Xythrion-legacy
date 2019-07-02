points = [('Users', 'Points'), ('Xithrius', 32), ('Xiux', 27)]
longest = max(map(len, [x[0] for x in points]))
points = [f'{x[0].rjust(longest)} : {x[1]}' for x in points]
print('\n'.join(str(y) for y in points))
