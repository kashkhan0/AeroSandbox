import pytest

import aerosandbox as asb
from aerosandbox.structures.beams import RectBar
import aerosandbox.numpy as np
import casadi as cas

from numpy.testing import assert_approx_equal

    
# %% RectBar tests

def test_rectbar1():
    
    opti = asb.Opti()
    beam = RectBar(
        opti=opti,
        init_geometry = {
            'height': 1,
            'width': 1,
            },
        length=10,
        points_per_point_load=50,
        bending=True,
        torsion=False
    )
    
    # Lock all vars
    beam.locked_geometry_vars = beam.req_geometry_vars
    
    lift_force = 100
    #load_location = 10
    
    #beam.add_point_load(load_location, np.array([-lift_force, 0, 0]))
    beam.add_distributed_load(force= np.array([-lift_force, 0, 0]), load_type='uniform')

    beam.setup()

    opti.minimize(beam.mass)

    p_opts = {}
    s_opts = {}
    s_opts["max_iter"] = 1e6  # If you need to interrupt, just use ctrl+c
    opti.solver('ipopt', p_opts, s_opts)

    try:
        sol = opti.solve()
        beam.substitute_solution(sol)
        beam.plot3D()
        beam.draw_geometry_vars()
    except:
        print("Failed!")
        sol = opti.debug
        print(sol)
        raise
    
# %%
# def test_tube1():
    
#     # TODO: Improve this test
    
#     opti = asb.Opti()
#     beam = Tube(
#         opti=opti,
#         length=60 / 2,
#         points_per_point_load=50,
#         geometry={'diameter_guess': 100, 'thickness': 0.14e-3 * 5},
#         bending=True,
#         torsion=False
#     )
#     lift_force = 9.81 * 103.873
#     load_location = opti.variable(15)
#     opti.subject_to([
#         load_location > 2,
#         load_location < 60 / 2 - 2,
#         load_location == 18,
#     ])
#     beam.add_point_load(load_location, -lift_force / 3)
#     beam.add_uniform_load(force=lift_force / 2)
#     beam.setup()

#     # Tip deflection constraint
#     opti.subject_to([
#         # beam.u[-1] < 2,  # Source: http://web.mit.edu/drela/Public/web/hpa/hpa_structure.pdf
#         # beam.u[-1] > -2  # Source: http://web.mit.edu/drela/Public/web/hpa/hpa_structure.pdf
#         beam.du * 180 / cas.pi < 10,
#         beam.du * 180 / cas.pi > -10
#     ])
#     opti.subject_to([
#         cas.diff(cas.diff(beam.nominal_diameter)) < 0.001,
#         cas.diff(cas.diff(beam.nominal_diameter)) > -0.001,
#     ])

#     # opti.minimize(cas.sqrt(beam.mass))
#     opti.minimize(beam.mass)
#     # opti.minimize(beam.mass ** 2)
#     # opti.minimize(beam.mass_proxy)

#     p_opts = {}
#     s_opts = {}
#     s_opts["max_iter"] = 1e6  # If you need to interrupt, just use ctrl+c
#     opti.solver('ipopt', p_opts, s_opts)

#     try:
#         sol = opti.solve()
#     except:
#         print("Failed!")
#         sol = opti.debug
        
#     beam.substitute_solution(sol)
    
#     assert_approx_equal(beam.mass, 12, significant=2)
    

if __name__ == '__main__':
    pytest.main()
