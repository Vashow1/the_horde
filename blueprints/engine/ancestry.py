#!/usr/bin/env python3
import json
import blueprints
from blueprints.community import Community
from blueprints.issue import Issue
from blueprints.debate import Debate
from blueprints import ISSUEFILE

"""
We start off with functions requested by Community and/or Issue
"""

OBJ_NONE = "Parsed a None object expected an horde object. Fail in ancestry module."

def getNamesFromFileOf(object_):
    """returns a list containing the ancestry of the object being requested"""
    if object_ is None:
        print(OBJ_NONE)
        return (None)
    class_ = object_.__class__.__name__
    filepath = f'ancestry_files/{class_}.lst'
    try:
        with open(filepath, 'r') as object_file:
            object_lst = object_file.read().split('_')
        return object_lst
    except FileNotFoundError:
        return []

def writeIdsToFile(filepath, sortedListOfIds):
    if len(sortedListOfIds) == 0:
        try:
            with open(filepath, 'w') as object_file:
                pass
            return
        except Exception as err:
            print(f"Failed to create file {filepath}. \nFunction Failed:\tapplication_requests.writeIdsToFile")
    sortedIdsString = '_'.join(sortedListOfIds)
    try:
        with open(filepath, 'w') as object_file:
            object_file.write(sortedIdsString)
    except Exception as err:
        print(f"Failed to print into {filepath}. \nFunction Failed:\tapplication_requests.writeIdsToFile")

def getObjectIndex(object_):
    """
    This function searches the index of an object for the <relationship_file> from a certain community
    using the binary search because the list of the <object_name> are a sorted array,
    we can search through them to find the starting point of a community's issues
    which is signified by an index containing the Community.ancestralName preceding it's issues
    which also contain their ancestral name head.
    returns the index of the <object_> in the <object_file> it is associated with
    and if it doesn't find it it returns None
    """
    if object_ is None:
        print(OBJ_NONE)
        return (None)
    sortedListOfObjectIds = getNamesFromFileOf(object_)
    low = 0
    high = len(sortedListOfObjectIds) - 1

    while low <= high:
        mid = (low + high) / 2
        guess = sortedListOfObjectIds[mid]

        if guess == object_.name:
            return mid
        if guess > object_.name:
            high = mid - 1
        else:
            low = mid + 1
    print("Object Missing in ancestry_files")
    return None

def giveObjectRelationship(object_):
    """
    This function traverses the tree that is
    the ISSUEFILE until it finds its members and
    slots itself in directed by the alphabetical order
    """
    filepath = f'ancestry_files/{object_.__class__.__name__}.lst' 
    if object_ is None:
        print(OBJ_NONE)
        return (None)
    obj_name = object_.name
    search_tree_names = getNamesFromFileOf(object_)
    if len(search_tree_names) == 0:
        search_tree_names.insert(0, object_.name)
        print("Placing object in ancestry")
        writeIdsToFile(filepath, search_tree_names)
        return (1)
    elif len(search_tree_names) == 1:
        if search_tree_names[0] > object_.name:
            search_tree_names.insert(0, object_.name)
        else:
            search_tree_names.insert(1, object_.name)
        print("Placing object in ancestry")
        writeIdsToFile(filepath, search_tree_names)
        return (1)

    low = 0
    high = len(search_tree_names) - 1

    while low <= high:
        mid = (low + high) / 2
        guess = search_tree_names[mid]

        if (guess < object_.name) and (search_tree_names[mid+1] > object_.name):
            search_tree_names.insert(mid + 1, object_.name)
            class_ = object_.__class__.__name__
            filepath = f'ancestry_files/{class_}.lst'
            print("Placing object in ancestry")
            writeIdsToFile(filepath, search_tree_names)
            return (1)
        if guess > object_.name:
            high = mid - 1
        else:
            low = mid + 1
        return (0)
    

def createCommunityIssuesArchive(community_):
    """
    This function is called while a community is being initialised
    Creates a community entry into the issues json file where all its
    Issues will be stored
    """
    filepath = f'ancestry_files/issues.json'
    issues_dict = {}
    community_name = community_.name
    if not isinstance(community_, Community):
        print("Instance is not Community")
        return False
    try:
        with open(filepath, 'r') as object_file:
            try:
                issues_dict = json.load(object_file)
            except json.JSONDecodeError as error:
                print(str(error))
                print("\n\nThis happened while trying to create a community entry into the issues' json file.\n\n")
                return False

    except FileNotFoundError:
        pass

    with open(filepath, 'w') as object_file:
            issues_dict[community_name] = []
            json.dump(issues_dict, object_file)
    return True

def getCommunityParentOf(instanceAncestralName):
    communityNameList = instanceAncestralName.split('_')[:-1]
    communityName = "_".join(communityNameList)
    return (communityName)

def checkIfObjectExists(objectName, className):
    """Checks if object is in the associated ancestry_file"""
    filepath = f'ancestry_files/{className}.lst'
    sortedListOfObjectIds = getNamesFromFileOf(eval(className))
    print(sortedListOfObjectIds)
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

def eraseObjectFamily(object_):
    """
    This function destroys the descendants history of an object_
    and finally erases itself from the <ancestry_file>
    """
    filepath = f'ancestry_files/{object_.__class__.__name__}.lst' 
    if object_ is None:
        print(OBJ_NONE)
        return (0)
    obj_name = object_.name
    search_tree_names = getNamesFromFileOf(object_)
    if len(search_tree_names) == 0:
        print("No Object in ancestry")
        return (0)
    elif len(search_tree_names) == 1:
        if search_tree_names[0] == object_.name:
            search_tree_names = ""
        else:
            print("No matching <object name> in ancestry files.")
            return
        print("Deleting <{object_.name}> from ancestry file")
        writeIdsToFile(filepath, search_tree_names)
        return (1)
    
    object_index = getObjectIndex(object_)
    search_tree_names.pop(object_index)
    writeIdsToFile(filepath, search_tree_names)

def writeIssueIntoJSON(issue_):
    """This function writes the issue instance into the ancestry_files/issue.json"""
    filepath = f"ancestry_files/issues.json"
    if not isinstance(issue_, Issue):
        print("Instance not Issue instance")
        return False
    issues_dict = {}
    try:
        with open(filepath, 'r') as object_file:
            try:
                issues_dict = json.load(object_file)
            except json.JSONDecodeError as error:
                print(str(error))
                print("\n\nThis happened while trying to create a community entry into the issues' json file.\n\n")
                return False

    except FileNotFoundError:
        pass

    with open(filepath, 'w') as object_file:
            issues_dict[issue_.parent].append(issue_.name)
            json.dump(issues_dict, object_file)
    return True

def getIssuesOfCommunity(community_name):
    """Gets all the issues ids for a particular community"""
    filepath = filepath = f"ancestry_files/issues.json"
    issues_dict = {}
    try:
        with open(filepath, 'r') as object_file:
            try:
                issues_dict = json.load(object_file)
            except json.JSONDecodeError as error:
                print(str(error))
                print("\n\nThis happened while trying to get issues related to a community in the issues' json file.\n\n")
                return []
    except FileNotFoundError:
        print("No issues.json file found. FAIL")
        return []
    try:
        issues_from_community = issues_dict['community_name']
        return (issues_from_community)
    except KeyError:
        print("Community not found")
        return []