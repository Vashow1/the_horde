#!/usr/bin/env python3
import blueprints
from blueprints.base_model import BaseModel

class Debate(BaseModel):
    parent = ""
    user_id = ""
    text = ""
    respondTo = ""

    def __init__(self, *args, **kwargs):
        """initiates a debate instance"""
        super().__init__(*args, **kwargs)
        self.name = self.parent  + '_' + self.__class__.__name__ + "." + self.id