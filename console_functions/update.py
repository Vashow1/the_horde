#!/usr/bin/env python3
"""
This module contains functions which are used to update attributes of
an object
"""
from blueprints import storage
def community(id_, **kwargs):
    """
    This updates a specific <Community> instance the attributes in **kwargs
    """
    permmissible_attributes = ['parents', 'title']
    all_current_obs = storage.all()

    if kwargs is None:
        print("Kwargs cannot be empty")
        return
    
    try:
        requested_obj = all_current_obs[f'Community.{id_}']
    except KeyError:
        print(f"Instance of id: {id_} not found")
        return


    for key, value in kwargs:
        if key not in permmissible_attributes:
            print("{key} is not a valid object key")
            return 
        requested_obj.__dict__.update({key: value})
    
    requested_obj.save()
    return (requested_obj)

def issue(id_, **kwargs):
    """
    This updates a specific <Issue> instance with the attributes in **kwargs
    """
    permmissible_attributes = ['parent', 'post']
    all_current_obs = storage.all()

    if kwargs is None:
        print("Kwargs cannot be empty")
        return

    try:
        requested_obj = all_current_obs[f'Issue.{id_}']
    except KeyError:
        print(f"Instance of id: {id_} not found")
        return
    
    for key, value in kwargs:
        if key not in permmissible_attributes:
            print("{key} is not a valid object key")
            return 
        requested_obj.__dict__.update({key: value})
    
    requested_obj.save()
    return (requested_obj)

def user(id_, **kwargs):
    """This updates a specific <User> instance with the attributes in **kwargs"""
    permmissible_attributes = ['phone_number', 'email', 'password']
    all_current_obs = storage.all()

    if kwargs is None:
        print("Kwargs cannot be empty")
        return

    try:
        requested_obj = all_current_obs[f'User.{id_}']
    except KeyError:
        print(f"Instance of id: {id_} not found")
        return
    
    for key, value in kwargs:
        if key not in permmissible_attributes:
            print("{key} is not a valid object key or immutable")
            return 
        requested_obj.__dict__.update({key: value})
    
    requested_obj.save()
    return (requested_obj)