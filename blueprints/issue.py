#!/usr/bin/env python3
"""This model describes the module of an issue"""
import blueprints
from blueprints.base_model import BaseModel


class Issue(BaseModel):
    """Class that stores various issues posted on a community"""
    parent = ""
    name = ""
    user_id = ""
    text = ""

    def __init__(self, *args, **kwargs):
        """Initialising the Issue"""
        super().__init__(*args, **kwargs)
        self.name = self.parent  + '_' + self.__class__.__name__ + "." + self.id
        self.for_against_tally = 0
        self.vote_count = 0
    
    def vote(self, ballot=False):
        """updates the for_against_tally"""
        if ballot:
            self.for_against_tally += 1
        else:
            self.for_against_tally -= 1

    def increaseVoteTally(self):
        """
        Increases the <vote_count> which will be essential
        in the for_you algorithm
        """
        self.vote_count += 1
    
    def decreaseVoteTally(self):
        self.vote_count -= 1
