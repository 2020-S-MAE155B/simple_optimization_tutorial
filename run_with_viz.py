# maximize L/D
# w.r.t. alpha
# s.t. CL >= CL*

# Model inputs: alpha, CL0, CD0, AR
# Model outputs: (L/D), CL

# Models:
# Component 1: alpha, CL0, CD0, AR
# Component 2: CL = CLa * alpha + CL0
# Component 3: CDi = CL^2 / (pi e AR)
# Component 4: CD = CD0 + CDi
# Component 5: L/D = CL/CD

import numpy as np
from openmdao.api import Group, IndepVarComp, ExecComp, ScipyOptimizeDriver
from simple_optimization.components.cl_comp import CLComp
from simple_optimization.components.cdi_comp import CDiComp

from lsdo_viz.api import Problem

prob = Problem()

model = Group()

comp = IndepVarComp()
comp.add_output('alpha', val=0.04)
comp.add_output('CLa', val=2 * np.pi)
comp.add_output('CL0', val=0.2)
comp.add_output('CD0', val=0.015)
comp.add_output('AR', val=8.)
comp.add_design_var('alpha', lower=0.)
model.add_subsystem('inputs_comp', comp, promotes=['*'])


comp = CLComp()
model.add_subsystem('cl_comp', comp, promotes=['*'])

e = 0.7
if 1:
    comp = CDiComp(e=e)
    model.add_subsystem('cdi_comp', comp, promotes=['*'])
else:
    from lsdo_utils.api import PowerCombinationComp
    comp = PowerCombinationComp(
        shape=(1,),
        out_name='CDi',
        coeff=1. / np.pi / e,
        powers_dict=dict(
            CL=2.,
            AR=-1.,
        )
    )
    model.add_subsystem('cdi_comp', comp, promotes=['*'])

comp = ExecComp('CD = CD0 + CDi')
model.add_subsystem('cd_comp', comp, promotes=['*'])

comp = ExecComp('LD = CL/CD')
comp.add_objective('LD', scaler=-1.)
model.add_subsystem('ld_comp', comp, promotes=['*'])

prob.model = model

prob.driver = ScipyOptimizeDriver()
prob.driver.options['optimizer'] = 'SLSQP'
prob.driver.options['tol'] = 1e-15
prob.driver.options['disp'] = True

prob.setup()
prob.run()

# prob.check_partials(compact_print=True)

print('alpha', prob['alpha'])
print('CL0', prob['CL0'])
print('CL', prob['CL'])
print('CD0', prob['CD0'])
print('CDi', prob['CDi'])
print('CD', prob['CD'])
print('LD', prob['LD'])