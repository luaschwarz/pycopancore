# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

"""
pycopancore
===========

Subpackages
-----------

None yet.

"""

<<<<<<< HEAD:pycopancore/cell/__init__.py
from .abstract_cell import Cell
from .abstract_planet import Planet
from .donut_world import DonutWorld
from .local_renewable_resource import RenewableResource
=======
from .integrator import Integrator
from .anthroposphere import Anthroposphere
from .macro_agents import MacroAgents
from .micro_agents import MicroAgents
from .ecosphere import Ecosphere
from .global_stocks import GlobalStocks
from .local_stocks import LocalStocks
>>>>>>> 8c33de86db0af8189344e4c6b6c0339ef90cdc7f:pycopancore/__init__.py


__author__ = "Jonathan F. Donges <donges@pik-potsdam.de>"
__copyright__ = \
    "Copyright (C) 2016 Jonathan F. Donges and COPAN team"
__license__ = "MIT license"
__url__ = "http://www.pik-potsdam.de/copan/software"
__version__ = "0.1.0"
__date__ = "2016-05-30"
__docformat__ = "restructuredtext en"
