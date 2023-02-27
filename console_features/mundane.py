#!/usr/bin/env python3
"""
This file contains functions which serve the console but are
too mundane to create there own modules
"""
import hashlib

def process_challenge_parameters(challenge_params):
    id_number = challenge_params[0]
    password = challenge_params[1]

    id_number_hashed = hashlib.sha256(id_number.encode())
    id_number = id_number_hashed.hexdigest()
    password_hashed = hashlib.sha256(password.encode())
    password = password_hashed.hexdigest()

    return (id_number, password)