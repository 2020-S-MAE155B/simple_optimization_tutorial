import numpy as np

from openmdao.api import Problem, IndepVarComp, Group

from simple_optimization.analysis_group import AnalysisGroup


my_shape = (1,)

prob = Problem()

analysis_group = AnalysisGroup(
    shape=my_shape,
)
prob.model.add_subsystem('cruise_analysis_group', analysis_group)

analysis_group = AnalysisGroup(
    shape=my_shape,
)
prob.model.add_subsystem('hover_analysis_group', analysis_group)

prob.model.connect('cruise_analysis_group.sonic_speed', 'hover_analysis_group.sonic_speed')

prob.setup(check=True)

prob['cruise_analysis_group.altitude'] = 500.
prob['hover_analysis_group.altitude'] = 3.
prob.run_model()

prob.model.list_outputs(prom_name=True)