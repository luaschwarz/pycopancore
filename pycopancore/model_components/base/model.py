"""base component's Model component mixin class and essential framework logics.

This class is the Model component mixin of the base model component and also
derives from ModelLogics.
"""

# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

# import essential framework logics
# (this import occurs ONLY in the base component):
from .model_logics import ModelLogics

from .. import abstract
from . import interface as I
from . import World, Cell, Nature, Individual, Culture, Society, \
    Metabolism


class Model (I.Model, abstract.Model, ModelLogics):
    """base model component mixin class.

    This is the base.Model class. It serves two purposes:
    1. Be the model class of the base component, providing the information
    about which mixins are to be used of the component AND:
    2. Provide the configure method via the parent class ModelLogics.
    """

    # specify entity types and process taxon classes 
    # defined in the base component:
    entity_types = [World, Cell, Individual, Society]
    process_taxa = [Nature, Culture, Metabolism]
