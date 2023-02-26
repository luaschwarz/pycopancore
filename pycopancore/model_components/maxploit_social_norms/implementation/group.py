"""Group entity type of the component maxploit_group_layer."""

# This file is part of pycopancore.
#
# Copyright (C) 2016-2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

from ...base import interface as B

from .. import interface as I
import numpy as np
from numpy.random import exponential, uniform

from .... import Explicit, Step

class Group(I.Group):
    """Define properties of maxploit_group_layer Group."""

    # process-related methods:

    def next_group_meeting_time(self, t):
        """Get the next meeting time"""
        return t + self.group_meeting_interval

    def group_update(self, unused_t):
        if not self.culture.fix_group_attitude:
            for g in self.world.groups:
                if uniform() < g.group_update_probability:
                    self.update_group_attitude(g)


    def update_group_attitude(self, group_j):
        """Update a groups attitude based on the mean_group_behaviour."""
        if self.culture.attitude_on:
            mean_group_value = self.mean_group_attitude
        else:
            mean_group_value = self.mean_group_behaviour
        if mean_group_value > self.culture.injunctive_majority_threshold: # get the mean in terms of true/false for adjusting the global attitude later
            group_j.group_attitude = 1
        else:
            group_j.group_attitude = 0


    def get_mean_group_attitude(self, unused_t):
        """Calculate the mean attitude of individuals in a group."""
        if list(self.mean_group_members):
            n = 0
            for i in self.group_members:
                if i.attitude:
                    n += 1
            N = len(list(self.group_members))
            self.mean_group_attitude = n/N

    def get_mean_group_behaviour(self, unused_t):
        """Calculate the mean behaviour of individuals in a group."""

        # check that group has members to prevent division by zero error
        if list(self.group_members):
            n = 0
            for i in self.group_members:
                if i.behaviour:
                    n += 1
            N = len(list(self.group_members))
            self.mean_group_behaviour = n/N

        # else: group keeps previous variable

    processes = [
        # Explicit("mean attitude in group", [I.Group.mean_group_attitude], get_mean_group_attitude),
        Explicit("mean behaviour in group", [I.Group.mean_group_behaviour], get_mean_group_behaviour),
        Step("update group attitude",
              [I.Group.group_attitude],
              [next_group_meeting_time,
               group_update])
    ]
