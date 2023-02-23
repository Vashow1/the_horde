#!/usr/bin/env python3
import blueprints
from blueprints.community import Community
from blueprints.issue import Issue
from blueprints.debate import Debate
from blueprints import ISSUEFILE

"""
We start off with functions requested by Community and/or Issue
"""

OBJ_NONE = "Parsed a None object expected an horde object. Fail in ancestry module."

def getNamesFromFileOf(**object_):
    """returns a list containing the ancestry of the object being requested"""
    if object_ is None or len(object) == 0:
        print(OBJ_NONE)
        return (None)
    class_ = object['__class__']
    filepath = f'ancestry_files/{class_}.lst'
    try:
        with open(filepath, 'r') as object_file:
            object_lst = object_file.read().split('_')
        return object_lst
    except FileNotFoundError:
        print("The relationship file is missing. GRAVE!!!")
        return []

def writeIdsToFileOf(filepath, sortedListOfIds):
    sortedIdsString = '_'.join(sortedListOfIds)
    try:
        with open(filepath, 'w') as object_file:
            object_file.write(sortedIdsString)
    except Exception as err:
        print(f"Failed to print into {filepath}. \nFunction Failed:\tapplication_requests.writeIdsToFileOf")

def getObjectIndex(**object_):
    """
    This function searches the index of an object for the <relationship_file> from a certain community
    using the binary search because the list of the <object_name> are a sorted array,
    we can search through them to find the starting point of a community's issues
    which is signified by an index containing the Community.ancestralName preceding it's issues
    which also contain their ancestral name head.
    returns the index of the <object_> in the <object_file> it is associated with
    and if it doesn't find it it returns None
    """
    if object_ is None or len(object) == 0:
        print(OBJ_NONE)
        return (None)
    sortedListOfObjectIds = getNamesFromFileOf(object_)
    low = 0
    high = len(sortedListOfObjectIds) - 1

    while low <= high:
        mid = (low + high) / 2
        guess = sortedListOfObjectIds[mid]

        if guess == object_.community_ancestral_name:
            return mid
        if guess > object_.community_ancestral_name:
            high = mid - 1
        else:
            low = mid + 1
    print("Object Missing in ancestry_files")
    return None

def giveObjectRelationship(**object_):
    """
    This function traverses the tree that is
    the ISSUEFILE until it finds its members and
    slots itself in directed by the alphabetical order
    """
    if object_ is None or len(object) == 0:
        print(OBJ_NONE)
        return (None)
    obj_name = object_['name']
    search_tree_names = getNamesFromFileOf(object_)
    low = 0
    high = len(search_tree_names) - 1

    while low <= high:
        mid = (low + high) / 2
        guess = search_tree_names[mid]

        if (guess < object_.community_ancestral_name) and (search_tree_names[mid+1] > object_.community_ancestral_name):
            search_tree_names.insert(mid + 1, object_.community_ancestral_name)
            class_ = object_['__class__']
            filepath = f'ancestry_files/{class_}.lst'
            writeIdsToFileOf(filepath, search_tree_names)
            return (1)
        if guess > object_.community_ancestral_name:
            high = mid - 1
        else:
            low = mid + 1
        return (0)
    
def getIssues(community_):
        """
        returns list of issue instances
        which belong to the community.
        """
        if community_ is None:
            print(OBJ_NONE)
            return (None)
        communityIssueIds = []
        idsOfallInstancesOfIssue = getNamesFromFileOf(Issue)

        startingPointForCommunityIssues = getObjectIndex(community_)
        i = startingPointForCommunityIssues
        while (getCommunityNameOf(idsOfallInstancesOfIssue[i]) != community_.communityName):
            communityIssueIds.append(idsOfallInstancesOfIssue[i])
            i += 1

def getCommunityNameOf(instanceAncestralName):
    communityNameList = instanceAncestralName.split('_')[:-1]
    communityName = "_".join(communityNameList)
    return (communityName)

def checkIfObjectExists(objectName, className):
    """Checks if object is in the associated ancestry_file"""
    filepath = f'ancestry_files/{className}.lst'
    sortedListOfObjectIds = getNamesFromFileOf(eval(className))
    low = 0
    high = len(sortedListOfObjectIds) - 1

    while low <= high:
        mid = (low + high) / 2
        guess = sortedListOfObjectIds[mid]
        if guess == objectName:
            return True
        if guess > objectName:
            high = mid - 1
        else:
            low = mid + 1
    return False