"""ODE process class.

ODE stands for Ordinary Differential Equation.
ODEs are used for continuos processes in which one of the variables is
dependent of the time.
"""

# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

#
# Imports
#


#
# Definition of class ODE
#

from ..private import _AbstractProcess


class ODE(_AbstractProcess):
    """Define ODE process class."""

    type = "ODE"
    timetype = "continuous"

    def __init__(self,
                 name,
                 variables,
                 specification,
                 *,
                 smoothness=1
                 ):
        """Initiate an instance of an ODE process.

        Parameters
        ----------
        name : string
        variables : list
            list of Variables whose time derivatives are added
            to by specification
        specification : func
            function(self,t) storing the derivatives in instance
            attributes d_varname, or list of sympy expressions giving the
            RHS of the equation(s)
        smoothness
        """
        super().__init__(name)

        self.variables = variables
        self.specification = specification
        self.smoothness = smoothness
