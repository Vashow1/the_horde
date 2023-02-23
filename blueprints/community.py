#!/usr/bin/env python3
"""
This module describes the class community
necessary methods to initiate and work with it
"""
import blueprints
from datetime import datetime
from blueprints.base_model import BaseModel
from blueprints.user import User

class Community(BaseModel):
    """
    Definition where all communities will be based
    """
    parent = ""
    Title = ""
    members = {}

    def __init__(self, *args, **kwargs):
        """Initializes city"""
        super().__init__(*args, **kwargs)
        self.name = self.parent  + '_' + self.__class__.__name__ + "." + self.id
    
    def addMember(self, user_):
        """Adds the <user_> instance to the community"""
        if not isinstance(user_, User):
            print(f"{str(user_)} is not an instance of User")
            return False
        self.members[user_.id] = user_.email
        return True
    
    def removeMember(self, user_):
        """Removes a member from the community"""
        if not isinstance(user_, User):
            print(f"{str(user_)} is not an instance of User")
            return False
        try:
            del self.members[user_.id]
            return True
        except KeyError:
            print("User is not a member of community. FAIL!")
            return False
        