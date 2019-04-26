def is_mod(pass_person):
    def wrapper(user):
        modList = ['this', 'that', 'another', 'Jennifer#8910']
        return
    return wrapper


@is_mod
def pass_person(aUser):
    print('test passed')


owner = 'Xithrius#1318'
user = 'Broshan#9342'
mod = 'Jennifer#8910'
pass_person('Jennifer#8910')

'''
aList = [5, 2, -3, 1, 6, 10]

def trace(sorting) :
   def wrapper(*args, **kwargs):
          print(*args, **kwargs)
          result = sorting(*args, **kwargs)
          print(*args, **kwargs)
   return wrapper

@trace
def sorting(aList) :
    aList.sort()

sorting(aList)
'''