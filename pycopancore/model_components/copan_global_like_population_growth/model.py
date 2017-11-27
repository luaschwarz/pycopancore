"""Model mixing class template.

TODO: adjust or fill in code and documentation wherever marked by "TODO:",
then remove these instructions
"""

# This file is part of pycopancore.
#
# Copyright (C) 2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

from . import interface as I
# import all needed entity type implementation classes:
from .implementation import SocialSystem
# import all needed process taxon implementation classes:
from .implementation import Metabolism


class Model (I.Model):
    """Model mixin class."""

    # mixins provided by this model component:

    entity_types = [SocialSystem]
    """list of entity types augmented by this component"""
    process_taxa = [Metabolism]
    """list of process taxa augmented by this component"""