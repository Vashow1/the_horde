#!/usr/bin/python3 
"""This module instantiates an object of class FileStorage"""
from blueprints.engine.file_storage import FileStorage

ISSUEFILE = 'object_files/issue_file.lst'
COMMUNITYFILE = 'object_files/community_file.lst'
storage = FileStorage()
storage.reload()