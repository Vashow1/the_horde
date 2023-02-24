#!/usr/bin/env python3
"""
This module contains functions that destroy either a <Community> or an <Issue> object
"""
from blueprints.community import Community
from blueprints.issue import Issue
from blueprints.debate import Debate
from blueprints.engine.ancestry import eraseObjectFamily, checkIfObjectExists

FAIL_OUTPUT = "Failed while trying to destroy object in the destroy module."
def communityBasedObject(class_name, object_id):
    """This function correctly destroys a <Community> or an <Issue> object"""

    if class_name is None or object_id is None:
        print("Cannot destroy None object")
        return

    object_identifier = class_name + '.' + object_id
    
    try:
       from blueprints import storage
       object_ = storage.all()[object_identifier]
    except ValueError:
        print("Object does not exist.")
        print(FAIL_OUTPUT)
        return None
    # Check if mother is valid
    if (object_.parent is not None):
        if (checkIfObjectExists(object_.parent, "Community") is False):
            print("object parent is not in ancestry files. FATAL!")
            print(FAIL_OUTPUT)
            return None
    successSigOfRelationshipDestruction = eraseObjectFamily(object_)
    if (successSigOfRelationshipDestruction):
        print("Successfully erased family of {class_name}.{object_id}")

    else:
        print("FATAL!")
        print(FAIL_OUTPUT)
        exit()
    
    try:
        del(storage.all()[object_identifier])
        storage.save()
    except KeyError:
        print ("no instance found")


def nonCommunityBasedObject(class_name="", object_id=""):
    """Destroys other objects"""
    if class_name == "":
        print("Missing class_name")
        print(FAIL_OUTPUT)

    if object_id == "":
        print("Missing object_id")
        print(FAIL_OUTPUT)
    object_identifier = class_name + '.' + object_id
    try:
        from blueprints import storage
        del(storage.all()[object_identifier])
        storage.save()
    except KeyError:
        print("no instance found")
