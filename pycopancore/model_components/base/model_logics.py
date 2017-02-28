"""base component's Model component mixin class plus essential framework logics 

This class is the Model component mixin of the base model component and also owns the configure
method. This method is central to the framework since it fuses together
the used classes and puts information about process types and variables
in special list to be accessed by the runner.
"""

# TODO: for clarity, move framework logics into separate class this class inherits from

# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

# only used in this component, not in others:
from pycopancore.model_components import abstract 
from pycopancore import Variable, ODE, Explicit, Step, Event, \
    _AbstractEntityMixin, _AbstractProcessTaxonMixin
import inspect

#
#  Define class Model
#


class ModelLogics (abstract.Model):
    """Model logics class
    
    Provide the configure method.
    The configure method has a very central role in the COPAN:core framework,
    it is called before letting run a model. It then searches which model class
    is used from the model module. It will then go through all components
    listed there and collect all variables and processes of said components.
    """

    components = None

    ODE_variables = None

    variables = None
    processes = None

    def __repr__(self):
        """Return a string representation of the base.Model."""
        # Is it necessary to list all objects? Or are classes sufficient?
        keys_entities = []
        keys_process_taxa = []
        for key, item in self.entities_dict:
            keys_entities.append(key)
        for key, item in self._process_taxon_objects:
            keys_process_taxa.append(key)
        return (super().__repr__() +
                ('base.model object with entities {} /'
                 'and process taxa {}'.format(keys_entities, keys_process_taxa)
                 )
                )

    #
    #  Definitions of further methods
    #

    @classmethod
    def configure(cls):
        """Configure the model.

        This classmethod configures the mixin models by allocating variables
        and processes to designated lists.
        """
        cls.variables = []  # save in pairs: (variable, owning_class)
        cls.processes = []  # save in pairs: (process, owning_class)

        cls.variables_dict = {}

        cls.process_variables = []

        cls.ODE_variables = []
        cls.explicit_variables = []
        cls.step_variables = []
        cls.event_variables = []

        cls.ODE_processes = []
        cls.explicit_processes = []
        cls.step_processes = []
        cls.event_processes = []

        print("\nConfiguring model", cls.name, "(", cls, ") ...")
        print("Analysing model structure...")

        # First analyse by component:
        parents = list(inspect.getmro(cls))[1:]
        cls.components = [c for c in parents
                          if c is not abstract.Model
                          and abstract.Model in inspect.getmro(c)
                          ]
        print('\nComponents:', cls.components)
        for c in cls.components:
            interfaceclass = c.__bases__[0]
            print("Model component:", interfaceclass.name, "(", c, ")...")
            # Iterate through all mixins of the component:
            for etmixin in c.entity_types:
                print('    Entity-type:', etmixin)
                cparents = list(inspect.getmro(etmixin))
                cvardict = {k: v
                            for cp in cparents
                            for (k, v) in cp.__dict__.items()
                            if isinstance(v, Variable)
                            }
                for (k, v) in cvardict.items():
                    print("        Variable:", v)
                    # check if same var. object was already registered:
                    if v in cls.variables_dict.values():
                        print("            already registered by another "
                              "component")
                        assert v._codename == k, ('with Codename', k)
                    if k in cls.variables_dict.keys():
                        print("            already registered by another "
                              "component")
                        assert cls.variables_dict[k] == v, \
                            'Codename already in use by another variable'
                    v._codename = k
                    cls.variables_dict[k] = v

                for p in etmixin.processes:
                    print("        Process:", p)

            # Iterate through all process taxon mixins:
            for pt in c.process_taxa:
                print('    Process taxon:', pt)
                cparents = list(inspect.getmro(pt))
                cvardict = {k: v
                            for cp in cparents
                            for (k, v) in cp.__dict__.items()
                            if isinstance(v, Variable)
                            }
                for (k, v) in cvardict.items():
                    print("        Variable:", v)
                    # check if same var. object was already registered:
                    if v in cls.variables_dict.values():
                        print("          already registered by another "
                              "component")
                        assert v._codename == k, ('with Codename', k)
                    if k in cls.variables_dict.keys():
                        print("          already registered by another "
                              "component")
                        assert cls.variables_dict[k] == v, \
                            'Codename already in use by another variable'
                    v._codename = k
                    cls.variables_dict[k] = v

                for p in pt.processes:
                    print("        Process:", p)

        # Now analyse by entity type and process taxon in order to find correct
        # owning classes:
        print('\nEntity types:', cls.entity_types)
        print('Process taxa:', cls.process_taxa)
        for owning_class in cls.entity_types + cls.process_taxa:
            print('    Entity-type/Process taxon:', owning_class)
            parents = list(inspect.getmro(owning_class))
            components = [c for c in parents
                          if issubclass(c, (_AbstractEntityMixin,
                                            _AbstractDynamicsMixin))
                          and c not in (_AbstractEntityMixin,
                                        _AbstractDynamicsMixin)
                          ]
            for mixin in components:
                print('        Mixin:', mixin)
                cparents = list(inspect.getmro(mixin))
                cvardict = {k: v
                            for cp in cparents
                            for (k, v) in cp.__dict__.items()
                            if isinstance(v, Variable)
                            }
                for (k, v) in cvardict.items():
                    v.owning_classes.append(owning_class)
                    if (v, owning_class) not in cls.variables:
                        print("        Variable:", v)
                        cls.variables.append((v, owning_class))
                for p in mixin.processes:
                    p.owning_classes.append(owning_class)
                    if (p, owning_class) not in cls.processes:
                        print("        Process:", p)
                        cls.processes.append((p, owning_class))

        for (process, owning_class) in cls.processes:
            cls.process_variables += [(v, owning_class) for v in
                                      process.variables]
            if isinstance(process, ODE):
                cls.ODE_variables += [(v, owning_class)
                                      for v in process.variables]
                cls.ODE_processes += [(process, owning_class)]
            elif isinstance(process, Explicit):
                cls.explicit_variables += [(v, owning_class)
                                           for v in process.variables]
                cls.explicit_processes += [(process, owning_class)]
            elif isinstance(process, Step):
                cls.step_variables += [(v, owning_class)
                                       for v in process.variables]
                cls.step_processes += [(process, owning_class)]
            elif isinstance(process, Event):
                cls.event_variables += [(v, owning_class)
                                        for v in process.variables]
                cls.event_processes += [(process, owning_class)]
            else:
                print('process-type of', process, 'not specified')
                print(process.__class__.__name__)
                print(object.__str__(process))

        print("...done")
        
    def convert_to_standard_units(self):
        """replace all variable values of type DimensionalQuantity 
        to float using the standard unit"""
        for var in self.variables:
            var.convert_to_standard_units()
            