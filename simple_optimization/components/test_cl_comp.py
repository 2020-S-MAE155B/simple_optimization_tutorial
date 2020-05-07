from openmdao.api import Problem
from openmdao.utils.assert_utils import assert_check_partials
from cl_comp import CLComp


prob = Problem()
prob.model = CLComp()

prob.set_solver_print(level=0)

prob.setup()
prob.run_model()

data = prob.check_partials(out_stream=None)
assert_check_partials(data, atol=1.e-6, rtol=1.e-6)

# try:
#     assert_check_partials(data, atol=1.e-6, rtol=1.e-6)
# except ValueError as err:
#     print(str(err))