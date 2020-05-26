from openmdao.api import Group, IndepVarComp

from lsdo_utils.api import PowerCombinationComp, LinearCombinationComp


class AerodynamicsGroup(Group):

    def initialize(self):
        self.options.declare('shape', types=tuple)

    def setup(self):
        shape = self.options['shape']
        
        comp = IndepVarComp()
        comp.add_output('C_L')
        comp.add_output('L_t', val=0.2)
        comp.add_output('area')
        self.add_subsystem('inputs_comp', comp, promotes=['*'])

        # L = CL^1 0.5 rho^1 V^2 S^1
        comp = PowerCombinationComp(
            shape=shape,
            out_name='L_w',
            coeff=0.5,
            powers_dict=dict(
                C_L=1.,
                density=1.,
                speed=2.,
                area=1.,
            )
        )
        self.add_subsystem('wing_lift_comp', comp, promotes=['*'])

        # L = 1. x L_w + 1. x L_t
        comp = LinearCombinationComp(
            shape=shape,
            out_name='L',
            constant=0.,
            coeffs_dict=dict(
                L_w=1.,
                L_t=1.,
            )
        )
        self.add_subsystem('total_lift_comp', comp, promotes=['*'])