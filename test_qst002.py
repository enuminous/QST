#!/usr/bin/env python3
"""Reproducible conditional math checks for QST-002, not physical validation."""
import math
import unittest
from base888_bridge import *

class QST002Tests(unittest.TestCase):
    def test_cycle_exact_spectrum(self):
        xs=laplacian_cycle()
        self.assertEqual(len(xs),888)
        self.assertAlmostEqual(xs[0],0.)
        self.assertAlmostEqual(xs[444],4.)
    def test_cycle_one_spatial_dimension(self):
        d=spectral_dimension(laplacian_cycle(),16.)
        self.assertTrue(.99<d<1.02, d)
    def test_stipulated_three_torus_is_not_emergent(self):
        xs=laplacian_torus()
        self.assertEqual(len(xs),888)
        self.assertTrue(2.8<spectral_dimension(xs,1)<3.2)
    def test_link_fluctuations(self):
        x=quantum_link(.5,1,2)
        self.assertAlmostEqual(x['mean_length'],1.5)
        self.assertAlmostEqual(x['variance'],.25)
        self.assertEqual(quantum_link(0)['variance'],0)
    def test_entangled_covariance(self):
        x=two_link_fluctuations(.5)
        self.assertAlmostEqual(x['two_independent_total_variance'],.5)
        self.assertAlmostEqual(x['two_entangled_total_variance'],1.)
    def test_anomaly_cancellation_if_SM_assumed(self):
        a=standard_model_anomalies()
        for name in ['U1_cubed','gravitational_U1','SU2_squared_U1','SU3_squared_U1','SU3_cubed']:
            self.assertEqual(a[name],'0',name)
        self.assertTrue(a['SU2_global_even_doublets'])
        self.assertEqual(a['states_selected']+a['unused_888_dimension'],888)
    def test_memory_mass_stability(self):
        x=massive_memory_normal_modes(1,2,.5)
        self.assertTrue(x['linearly_stable'])
        self.assertAlmostEqual(x['omega_sq_minus']+x['omega_sq_plus'],5.)
        bad=massive_memory_normal_modes(1,1,2)
        self.assertFalse(bad['linearly_stable'])
    def test_finite_ccr_no_go(self):
        o=ccr_finite_dimension_obstruction()
        self.assertFalse(o['exact_canonical_CCR_possible'])
        self.assertEqual(o['imaginary_part_of_i_identity_trace'],888)
        self.assertAlmostEqual(o['frobenius_residual_lower_bound_hbar_1'],math.sqrt(888))
    def test_graviton_EFT_not_base888(self):
        x=effective_graviton_oscillator(2)
        self.assertAlmostEqual(x['vacuum_variance_q'],.25)
        self.assertEqual(x['count_TT_helicities'],2)

if __name__=='__main__':unittest.main(verbosity=2)
