#!/usr/bin/env python3
"""This module describe the user object"""
import blueprints
from blueprints.base_model import BaseModel
from blueprints.issue import Issue


class User(BaseModel):
    """This class defines a user utilising its various attributes"""
    email = ""
    password = ""
    id_number = ""
    phone_number = ""
    issues_voted_on = {}
    communities_joined = []

    def __init__(self, kwargs):
        """Initiates a user"""
        super().__init__(kwargs)
    
    def voteFor(self, issue_):
        """
        Increases the for votes on an issue
        """
        issue_id = issue_.id
        if issue_id in self.issues_voted_on.keys():
            if self.issues_voted_on[issue_id]:
                del self.issues_voted_on[issue_id]
                issue_.vote(False)
                issue_.decreaseVoteTally()
            else:
                self.issues_voted_on[issue_id] = True
                issue_.vote(True)
        else:
            issue_.vote(True)
            issue_.increaseVoteTally()
            self.issues_voted_on[issue_id] = True
    
    def voteAgainst(self, issue_):
        """
        Increases the against votes on an issue
        """
        issue_id = issue_.id
        if issue_id in self.issues_voted_on.keys():
            if not self.issues_voted_on[issue_id]:
                del self.issues_voted_on[issue_id]
                issue_.vote(True)
                issue_.decreaseVoteTally()
            else:
                self.issues_voted_on[issue_id] = False
                issue_.vote(False)
        else:
            issue_.vote(False)
            issue_.increaseVoteTally()
            self.issues_voted_on[issue_id] = False
    
    def joinCommunity(self, community_id):
        """Adds the community to the list of user's community memberships"""
        try:
            from blueprints import storage
            community_joining = storage.all()[f"Community.{community_id}"]
        except KeyError:
            print("community is non-existent")
            return False
        self.communities_joined.append(community_id)
        return True

    def leaveCommunity(self, community_id):
        """Removes the community from the list of user's community memberships"""
        try:
            from blueprints import storage
            community_leaving = storage.all()[f"Community.{community_id}"]
        except KeyError:
            print("community is non-existent")
            return False
        self.communities_joined.remove(community_id)
        return True
    

        
