#!/usr/bin/env python3
from blueprints.community import Community
from blueprints.issue import Issue
from blueprints.debate import Debate
from blueprints.user import User
from blueprints.engine.ancestry import giveObjectRelationship, checkIfObjectExists
import hashlib
"""Contains functions responsible for the logic behind creation of objects"""
FAIL_OUTPUT = "Failed while trying to create object in the creation module."
def community(**kwargs):
    """This function correctly initialises a <Community>, <Issue> and <Debate> instance"""

    parameters = ['parents', 'title']
    object_dictionary = {}
    if kwargs is None:
        print("Kwargs cannot be empty")
        return
    if sorted(parameters) != sorted(kwargs.keys()):
        print("wrong parametes. FAIL")
        return
    try:
        community_parent = kwargs['parent']
        if community_parent is None or community_parent == "":
            print("Please specify the <param> param (mother of the community)")
            print(FAIL_OUTPUT)
            return None
        
    except ValueError:
        print("Please specify the <parent> param")
        print(FAIL_OUTPUT)
        return None
    # Check if mother is valid
    if checkIfObjectExists(community_parent, "Community") is False:
        print("<parent> is non-existent. FATAL! Creation cancelled")
        print(FAIL_OUTPUT)
        return None
    kwargs['__class__'] = "Community"
    newCommunity = Community(kwargs)
    successSigOfRelationshipCreation = giveObjectRelationship(newCommunity.to_dict())
    if (successSigOfRelationshipCreation):
        return (newCommunity)

def issue(**kwargs):
    """This function correctly initialises an <Issue> instance"""
    parameters = ['parent', 'post']
    object_dictionary = {}
    if kwargs is None:
        print("Kwargs cannot be empty")
        return
    if sorted(parameters) != sorted(kwargs.keys()):
        print("wrong parametes. FAIL")
        return
    issue_parent = kwargs['parent']
    if issue_parent is None or issue_parent == "":
        print("Please populate the <parent> param (mother of the community)")
        print(FAIL_OUTPUT)
        return None
    # Check if mother is valid
    if checkIfObjectExists(issue_parent, "Issue") is False:
        print("<parent> is non-existent. FATAL! Creation cancelled")
        print(FAIL_OUTPUT)
        return None
    kwargs['__class__'] = "Issue"
    newIssue = Issue(kwargs)
    successSigOfRelationshipCreation = giveObjectRelationship(newIssue.to_dict())
    if (successSigOfRelationshipCreation):
        return (newIssue)
    
def user(**kwargs):
    """This function correctly initialises a <User> instance"""
    parameters = ['id_number', 'phone_number', 'email', 'password']
    object_dictionary = {}
    if kwargs is None:
        print("Kwargs cannot be empty")
        return
    if sorted(parameters) != sorted(kwargs.keys()):
        print("wrong parametes. FAIL")
        return
    password = kwargs['password']
    hashed = hashlib.sha256(password.encode())
    passwordHexadecimal = hashed.hexdigest()
    kwargs['password'] = passwordHexadecimal
    new_user = User(kwargs)