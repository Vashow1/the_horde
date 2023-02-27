#!/usr/bin/env python3
"""
This module works on processing of creation
of users and the consequent saving of passwords.

"""
import json
filepath = "./guarded.scrt"
from blueprints.user import User

def create_challenge(user_, password) -> bool:
    """
    This function takes in a user_instance and populates a file
    to store id-password values.
    """
    if not isinstance(user_, User) or user_ is None:
        print("Cannot create challenge with wrong inputs.")
        return False
    
    id_number = user_.id_number
    instance_id = user_.id
    challenge = []
    hashes = {}

    challenge = [instance_id, password]
    try:
        with open(filepath, mode="r", encoding="utf-8") as guarded_file:
            hashes = json.load(guarded_file.read())
    except FileNotFoundError:
        pass
    
    if hashes.get(id_number) is not None:
        print("User exists already.")
        return False
    hashes[id_number] = challenge
    with open(filepath, mode="w", encoding="utf-8") as guarded_file:
        json.dump(hashes, guarded_file)
    return True

def solve_challenge(challenge_params) -> User:
    """
    This function takes in the id_number and password of user
    and returns the user instance of the id
    """
    id_number = challenge_params[0]
    password = challenge_params[1]
    
    try:
        with open(filepath, mode="r", encoding="utf-8") as guarded_file:
            hashes = json.load(guarded_file)
    except FileNotFoundError:
        print("No user exists in the guarded files")
        return None
    try:
        user_data = hashes[id_number]
        instance_id = user_data[0]
        instance_answer = user_data[1]
    except KeyError:
        print(f"No user with id_number {id_number}")
        return
    if password == instance_answer:
        from blueprints import storage
        new_user = storage.all()[f'User.{instance_id}']
        return (new_user)
    else:
        print("Wrong password.")
        return None
