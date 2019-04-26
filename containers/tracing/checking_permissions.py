'''

+----[ Relay.py ]-------------------------------+
|                                               |
|  Copyright (c) 2019 Xithrius                  |
|  MIT license, Refer to LICENSE for more info  |
|                                               |
+-----------------------------------------------+

'''


# //////////////////////////////////////////////////////////////////////////// #
# Libraries                                                                    #
# //////////////////////////////////////////////////////////////////////////// #
# Built-in modules, third-party modules, custom modules                        #
# //////////////////////////////////////////////////////////////////////////// #


from containers.essentials.pathing import path


# //////////////////////////////////////////////////////////////////////////// #
# Tracing permissions
# //////////////////////////////////////////////////////////////////////////// #
# Checking the caller and condition of command to decide if runnable
# //////////////////////////////////////////////////////////////////////////// #


class Tracing_Permissions():

    def __init__(self, user):
        self.user = user

    async def is_allowed(self):
        def wrapper():
            pass



'''

def requires_admin(fn):
    def ret_fn(*args,**kwargs):
        lPermissions = get_permissions(current_user_id())
        if 'administrator' in lPermissions:
            return fn(*args,**kwargs)
        else:
            raise Exception("Not allowed")
    return ret_fn

def requires_logged_in(fn):
    def ret_fn(*args,**kwargs):
        lPermissions = get_permissions(current_user_id())
        if 'logged_in' in lPermissions:
            return fn(*args,**kwargs)
        else:
            raise Exception("Not allowed")
    return ret_fn
    
def requires_premium_member(fn):
    def ret_fn(*args,**kwargs):
        lPermissions = get_permissions(current_user_id())
        if 'premium_member' in lPermissions:
            return fn(*args,**kwargs)
        else:
            raise Exception("Not allowed")
    return ret_fn
    
@requires_admin
def delete_user(iUserId):
   """
   delete the user with the given Id. This function is only accessable to users with administrator permissions
   """

@requires_logged_in 
def new_game():
    """
    any logged in user can start a new game
    """
    
@requires_premium_member
def premium_checkpoint():
   """
   save the game progress, only accessable to premium members
   """

'''