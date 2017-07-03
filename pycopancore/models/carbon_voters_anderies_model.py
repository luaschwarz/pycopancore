"""Model class carbon_voters_anderies_model."""

# This file is part of pycopancore.
#
# Copyright (C) 2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

#
#  Imports
#

from .. import base  # all models must use the base component

from ..model_components import adaptive_voter_opinion_formation as avof
from ..model_components import majority_decision as md
from ..model_components import anderies_carbon_cycle as cc
from ..model_components import carbon_voters as cv


# entity types:

# NEED TO: compose all needed entity type implementation classes
# by mixing the above model components' mixin classes of the same name.
# Only compose those entity types and process taxons that the model needs,
# delete the templates for the unneeded ones, and add those for missing ones:

# NEED TO: list all mixin classes needed:
class World(cc.World,
            cv.World,
            base.World):
    """World entity type."""

    pass


# NEED TO: list all mixin classes needed:
class Society(md.Society,
              cv.Society,
              cc.Society,
              base.Society):
    """Society entity type."""

    pass


# NEED TO: list all mixin classes needed:
class Cell(cc.Cell,
           base.Cell):
    """Cell entity type."""

    pass


# NEED TO: list all mixin classes needed:
class Individual(avof.Individual,
                 md.Individual,
                 base.Individual):
    """Individual entity type."""

    pass


# process taxa:

# NEED TO: do the same for process taxa:


# NEED TO: list all mixin classes needed:
class Nature(cc.Nature,
             base.Nature):
    """Nature process taxon."""


# NEED TO: list all mixin classes needed:
class Metabolism(base.Metabolism):
    """Metabolism process taxon."""

    pass


# NEED TO: list all mixin classes needed:
class Culture(avof.Culture,
              cv.Culture,
              base.Culture):
    """Culture process taxon."""

    pass


# Model class:

# NEED TO: list all used model components:
class Model(avof.Model,
            md.Model,
            cc.Model,
            cv.Model,
            base.Model):
    """Class representing the whole model."""

    name = "..."
    """Name of the model"""
    description = "..."
    """Longer description"""

    # NEED TO: list all entity types you composed above:
    entity_types = [World, Society, Individual, Cell]
    """List of entity types used in the model"""
    # NEED TO: list all entity types you composed above:
    process_taxa = [Culture, Nature]
    """List of process taxa used in the model"""
