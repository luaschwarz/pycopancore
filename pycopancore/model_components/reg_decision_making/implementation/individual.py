"""Individual entity type class template.

TODO: adjust or fill in code and documentation wherever marked by "TODO:",
then remove these instructions
"""

# This file is part of pycopancore.
#
# Copyright (C) 2016-2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license
import numpy as np

from enum import Enum
from random import sample

from pycopancore.process_types import Step
from pycopancore.model_components.base import interface as B
import pycopancore.model_components.base as base

from .. import interface as I


class AFT(Enum):
    """Available Inputs"""
    progressive_minded: int = 0
    conservative_minded: int = 1

    @staticmethod
    def random():
        return sample(list(AFT), 1)[0]


class Individual (I.Individual, base.Individual):
    """Individual entity type mixin implementation class."""

    # standard methods:

    # aufgeführt: alle allgemeinen parameter, und AFT-spezifische parameter
    # für den "traditionalist" type
    def __init__(self,
                 *,
                 aft=AFT.random(),
                 config=None,
                 avg_hdate=0,
                 **kwargs):

        """Initialize an instance of Individual."""
        super().__init__(**kwargs)  # must be the first line

        self.aft = aft
        self.__dict__.update(getattr(config.aftpar, self.aft.name).to_dict())
        self.behaviour = self.cell.input[config.couple_target[0]]

        # average harvest date of the cell is used as a proxy for the order
        # of the agents making decisions in time through the year
        self.avg_hdate = avg_hdate

        # soilc is the last "measured" soilc value of the farmer whereas the
        #   cell_soilc value is the actual status of soilc of the cell
        self.soilc = self.cell_soilc

        # Same applies for cropyield (as for soilc)
        self.cropyield = self.cell_cropyield
        # Maximal soilc and cropyield might be used in the future to assess
        #   soil potential
        # self.max_soilc = self.soilc
        # self.max_cropyield = self.cropyield

    def init_neighbourhood(self):
        """Initialize the neighbourhood of the agent."""
        self.neighbourhood = [
            neighbour for cell_neighbours in self.cell.neighbourhood
            if len(cell_neighbours.individuals) > 0
            for neighbour in cell_neighbours.individuals
        ]

    @property
    def cell_cropyield(self):
        return self.cell.output.pft_harvestc.values.mean()

    @property
    def cell_soilc(self):
        return self.cell.output.soilc.values.mean()

    @property
    def attitude(self):
        return self.weight_social_learning * \
                self.attitude_social_learning \
                + self.weight_own_land * self.attitude_own_land

    # calculating the input of farmer's own land evaluation to attitude
    # differentiated for 2 farmer types
    @property
    def attitude_own_land(self):
        # TODO differentiate for 2 AFTs
        # TODO think about to which tate agent compares current state...
        # state before last update or last year?
        # See definition for soilc and cell_soilc in init
        attitude_own_soil = sigmoid(self.soilc -
                                    self.cell_soilc)
        # See definition for cropyield and cell_cropyield in init
        attitude_own_yield = sigmoid(self.cropyield -
                                     self.cell_cropyield)
        return attitude_own_soil, attitude_own_yield

    # calculating the input of farmer's comparison to neighbouring farmers
    # to attitide, differentiated for 2 farmer types
    @property
    def attitude_social_learning(self):
        # maybe split up method above? or explicitly refer to the valsneeded?
        average_cropyields = self.split_neighbourhood_status("cropyield")
        average_soilcs = self.split_neighbourhood_status("soilc")
        # important: this is about behaviour (RA / CF, NOT AFT)
        yields_diff, yields_same = average_cropyields[not self.behaviour],\
            average_cropyields[self.behaviour]
        soils_diff, soils_same = average_soilcs[not self.behaviour],\
            average_soilcs[self.behaviour]
        # TODO is agent_i.behaviour really getting me to the right return?

        # calc both yield and soil comparison, then weight
        # TODO think about sigmoid instead of heaviside?
        yield_comparison = yields_diff - self.get_yield() *\
            np.heaviside(yields_diff - yields_same, 0)
        soil_comparison = soils_diff - self.get_soil_carbon() *\
            np.heaviside(soils_diff - soils_same, 0)

        return sigmoid(self.weight_yield * yield_comparison +
                       self.weight_soil * soil_comparison)

    """The social learning part of TPB here looks at the average behaviour,
    not performance, of neighbouring agents"""
    @property
    # calculating descriptive social norm based on all neighbouring farmers
    def social_norm(self):
        # TODO check if base model is neede for .neighbours
        social_norm = 0
        if self.neighbourhood:
            social_norm = (
                sum(n.behaviour for n in self.neighbourhood) /
                len(self.neighbourhood)
            )
        if self.behaviour == 1:
            return sigmoid(0.5-social_norm)
        else:
            return sigmoid(social_norm-0.5)

    # TODO: how to do this for the two AFTs?
    @property
    def random_behaviour(self):
        """compute a random farming behaviour of individual"""
        return np.random.rand()

    def split_neighbourhood(self, attribute):
        first_nb = []  # regeneratively managed
        second_nb = []  # conventionally managed
        for neighbour in self.neighbourhood:
            if getattr(neighbour, attribute) == 1:
                first_nb.append(neighbour)
            else:
                second_nb.append(neighbour)
        return first_nb, second_nb

    def split_neighbourhood_status(self, variable):
        # sorting agent_i neighbours by their current farming behaviour
        # (regenerative or conventional)
        # note: current behavoor is not necessarily = farmer type
        # calculate average yield for neighbours, reg. and conv.
        # TODO think about finding a nicer way to access list_neighbours outputs
        first_nb, second_nb = self.split_neighbourhood("behaviour")
        if first_nb:
            first_var = sum(getattr(n, variable) for n in first_nb)\
                / len(first_nb)
        else:
            first_var = 0
        # for conventionals
        if second_nb:
            second_var = sum(getattr(n, variable) for n in second_nb)\
                / len(second_nb)
        else:
            second_var = 0

        return first_var, second_var

    def update_behaviour(self, t):
        # now comes the update
        # identity_value = 0
        tpb = (self.weight_attitude * self.attitude
               + self.weight_norm * self.calc_social_norm())\
            * self.pbc

        if np.random.random() < tpb:
            self.cropyield = self.cell_cropyield
            # self.max_crop_yield = max(self.max_crop_yield, self.cropyield)
            self.soilc = self.cell_soilc
            # self.max_soilc = max(self.max_soilc, self.soilc)
            self.behaviour = int(not self.behaviour)
            self.set_cell_input(self.behaviour)

    def set_cell_input(self, value):
        self.cell.input[self.couple_target] = value

    processes = [
        Step("update farmer",
             [I.Individual.behaviour],
             [update_behaviour])
    ]


def sigmoid(x):
    """The following part contains helping stuff"""
    return 0.5 * (np.tanh(x) + 1)
