#!/usr/bin/env python3
import json
from blueprints.issue import Issue
from blueprints.community import Community
from blueprints.user import User
from blueprints.debate import Debate



classes = {"Issue": Issue, "Community": Community, "User": User}

class FileStorage:
    """This class manages the storage of the horde class objects in JSON format"""
    __file_path = 'anons.json'
    __objects = {}
    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        if cls is None:
            return FileStorage.__objects
        else:
           return {k: v for (k, v) in FileStorage.__objects.items()
                    if cls == v.__class__ or cls == v.__class__.__name__}
    
    def new(self, object_):
        """Adds a new object to the storage dictionary"""
        if object_ is not None:
            key = object_.__class__.__name__ + "." + object_.id
            self.__objects[key] = object_
    
    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__objects) as objects_file:
            cached_objects = {}
            cached_objects.update(FileStorage.__objects)
            for key, val in cached_objects.items():
                cached_objects[key] = val.to_dict()
            json.dump(cached_objects, objects_file)
        
    
    def reload(self):
        """Loads storage dictionary from file"""
        try:
            cached_objects = {}
            with open(FileStorage.__file_path, 'r') as object_file:
                cached_objects = json.load(object_file)

            for key, val in cached_objects.items():
                object_ = classes[val['__class__']](**cached_objects[key]) # Initializing an object from the dict
                self.__objects[key] = object_

        except FileNotFoundError:
            pass
    
    def delete(self, object_=None):
        """
        Deletes an object from __objects if present
        if object_ is equal to None, the method should do nothing
        """
        if object_ is None:
            return
        for k, v in FileStorage.__objects.items():
            if v is object_:
                del FileStorage.___objects[k]
                self.save()
                return
        
    
    def close(self):
        """Calls reload() method for deserializing the JSON file to objects"""
        self.reload()
    
    def get(self, class_, id):
        """Retrieves an object"""
        object_key = class_.__class__ + '.' + id
        if class_ is None or class_ not in classes.values():
            return None
    
        try:
            requested_object = self.__object[object_key]
            return requested_object
        except KeyError:
            return None
