"""
Social sub-component of the InSEEDS model.
This does not inlude any communication to LPJmL via the pycoupler, but can be 
regarded as a first step towards coupled runs.

Based on the exploit model, inluding novel decision-making dynamics
on tha basis of the Theory of Planned behaviour (TPB)

Conceptualization by Luana Schwarz, implementation based on Ronja Hotz' 
Exploit model MOL CC SN, with adjustments by Luana Schwarz.

TODO: Go through the file and adjust all parts of the code marked with the TODO
flag. Pay attention to those variables and object written in capital letters.
These are placeholders and must be adjusted as needed. For further details see
also the model development tutorial.
"""
# This file is part of pycopancore.
#
# Copyright (C) 2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>

#
# TODO: import all other needed model components (adjust as needed):
#
import pycopancore.model_components.base as base
import pycopancore.model_components.reg_decision_making as decision_making


# entity types:

# TODO: compose all needed entity type implementation classes
# by mixing the above model components' mixin classes of the same name.
# Only compose those entity types and process taxons that the model needs,
# delete the templates for the unneeded ones, and add those for missing ones:

# TODO: list all mixin classes needed:
class World(base.World):
    """World entity type."""
    pass


# TODO: list all mixin classes needed:
class SocialSystem(base.SocialSystem):
    """SocialSystem entity type."""
    pass


# TODO: list all mixin classes needed:
class Cell(decision_making.Cell,  # TODO why is cell not linked?
           base.Cell):
    """Cell entity type."""
    pass


# TODO: list all mixin classes needed:
class Individual(decision_making.Individual,
                 base.Individual):
    """Individual entity type."""
    pass


# process taxa:

# TODO: do the same for process taxa:

# TODO: list all mixin classes needed:



# TODO: list all mixin classes needed:
class Culture(decision_making.Culture,
              base.Culture):
    """Culture process taxon."""
    pass


# Model class:

# TODO: list all used model components:
class Model(decision_making.Model,
            base.Model):
    """Class representing the whole model."""

    name = "InSEEDS Social"
    description = "Subcomponent of the InSEEDS model representing only social \
    dynamics and decision-making on the basis of the TPB"

    # TODO: list all entity types you composed above:
    entity_types = [World, SocialSystem, Cell, Individual]
    """List of entity types used in the model"""

    # TODO: list all entity types you composed above:
    process_taxa = [Culture]
    """List of process taxa used in the model"""