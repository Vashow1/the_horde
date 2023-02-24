#!/usr/bin/env python3
"""Contains functions responsible for the logic behind creation of objects"""
from blueprints.community import Community
from blueprints.issue import Issue
from blueprints.debate import Debate
from blueprints.user import User
from blueprints.engine.ancestry import giveObjectRelationship, checkIfObjectExists, createCommunityIssuesArchive, writeIssueIntoJSON
import hashlib


FAIL_OUTPUT = "Failed while trying to create object in the create module."
def community(kwargs):
    """This function correctly initialises a <Community>, <Issue> and <Debate> instance"""

    if not isinstance(kwargs, dict):
        print("The parameter is not a dictionary")
        return

    parameters = ['parent', 'title']
    object_dictionary = {}
    if kwargs is None:
        print("Kwargs cannot be empty")
        return
    if sorted(parameters) != sorted(kwargs.keys()):
        print("wrong parametes. FAIL")
        return
    try:
        community_parent = kwargs['parent']
    except ValueError:
        print("Please specify the <parent> param")
        print(FAIL_OUTPUT)
        return None
    # Check if mother is valid
    if (community_parent is not None):
        if (checkIfObjectExists(community_parent, "Community") is False):
            print("<parent> is non-existent. FATAL! Creation cancelled")
            print(FAIL_OUTPUT)
            return None
    kwargs['__class__'] = "Community"
    newCommunity = Community(kwargs)
    successSigOfRelationshipCreation = giveObjectRelationship(newCommunity)
    if (successSigOfRelationshipCreation and createCommunityIssuesArchive(newCommunity)):
        return (newCommunity)

def issue(kwargs):
    """This function correctly initialises an <Issue> instance"""
    if not isinstance(kwargs, dict):
        print("The parameter is not a dictionary")
        return
    
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
    
    kwargs['__class__'] = "Issue"
    new_issue = Issue(kwargs)
    if writeIssueIntoJSON(issue_):
        return (new_issue)
    
    else:
        print("Failed in updating Issue's into JSON")
        return None

def user(kwargs):
    """This function correctly initialises a <User> instance"""
    
    if not isinstance(kwargs, dict):
        print("The parameter is not a dictionary")
        return
    
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
    return (new_user)