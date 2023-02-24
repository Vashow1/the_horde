#!/usr/bin/env python3
"""
Describes the template for creation, deletion and serialization
of other objects
"""
import blueprints
from datetime import datetime
import uuid

class BaseModel:
    """
    Definition where all classes will be based
    """
    def __init__(self, kwargs=None):
        """Instatiates a new model"""
        time_format = '%Y-%m-%dT%H:%M:%S.%f'
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = self.created_at

        else:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
            if "id" not in kwargs.keys():
                self.id = str(uuid.uuid4())
            if kwargs.get("created_at") and type(self.created_at) is str:
                self.created_at = datetime.strptime(kwargs['created_at'], time_format)
            else:
                self.created_at = datetime.utcnow()
        
            if kwargs.get("created_at") and type(self.created_at) is str:
                self.updated_at = datetime.strptime(kwargs['updated_at'], time)
            else:
                self.updated_at = datetime.utcnow()
    
    def __str__(self):
        """Returns a string representation of the instance"""
        class_name = self.__class__.__name__
        return f"[{class_name}] ({self.id}) {self.__dict__}"  

    def to_dict(self):
        """Convert instance into dict format"""
        instances_dict = {}
        instances_dict.update(self.__dict__)
        instances_dict.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        instances_dict['created_at'] = self.created_at.isoformat()
        instances_dict['updated_at'] = self.updated_at.isoformat()
        if '_sa_instance_state' in instances_dict.keys():
            del instances_dict['_sa_instance_state']
        return (instances_dict)

    def delete(self):
        """deletes the current instance from the storage"""
        blueprints.storage.delete(self)
