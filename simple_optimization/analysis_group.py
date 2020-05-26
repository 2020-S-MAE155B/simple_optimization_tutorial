from openmdao.api import Group, IndepVarComp

from lsdo_aircraft.atmosphere.atmosphere import Atmosphere
from lsdo_aircraft.atmosphere.atmosphere_group import AtmosphereGroup

from simple_optimization.aerodynamics_group import AerodynamicsGroup


class AnalysisGroup(Group):

    def initialize(self):
        self.options.declare('shape', types=tuple)

    def setup(self):
        shape = self.options['shape']
        
        comp = IndepVarComp()
        comp.add_output('altitude')
        comp.add_output('speed')
        self.add_subsystem('inputs_comp', comp, promotes=['*'])

        atmosphere = Atmosphere(
            name='atmosphere',
        )
        group = AtmosphereGroup(
            shape=shape,
            options_dictionary=atmosphere,
        )
        self.add_subsystem('atmosphere_group', group, promotes=['*'])

        group = AerodynamicsGroup(
            shape=shape,
        )
        self.add_subsystem('aerodynamics_group', group, promotes=['*'])