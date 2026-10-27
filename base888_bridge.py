#!/usr/bin/env python3
"""QST-002: exact finite quantum-geometry and SM anomaly diagnostics.

This demonstrates conditional mathematics only. Geometry is stipulated by
choosing a graph; the Standard Model's representations are also stipulated.
Neither spacetime nor Standard Model emergence is derived here.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as F
import json
import math

N=888
SHAPE_3=(8, 3, 37) # 8*3*37 = 888; an assumed 3D torus, not emergent spacetime


def laplacian_cycle(n:int=N):
    if n<3: raise ValueError('Cycle must have >= 3 vertices')
    return [4*math.sin(math.pi*k/n)**2 for k in range(n)]


def laplacian_torus(shape=SHAPE_3):
    if math.prod(shape) != N: raise ValueError('Expected 888 total sites')
    # Spectrum of Cartesian product of periodic cycles.
    vals=[0.]
    for n in shape:
        axis=laplacian_cycle(n)
        vals=[v+a for v in vals for a in axis]
    return vals


def spectral_dimension(eigenvalues:list[float],tau:float)->float:
    if tau<=0: raise ValueError('Diffusion time must be positive')
    weights=[math.exp(-tau*x) for x in eigenvalues]
    z=sum(weights)
    return 2*tau*sum(x*w for x,w in zip(eigenvalues,weights))/z


def quantum_link(p:float,low:float=1.,high:float=2.):
    """Two sectors of 888=2*444 encode two discrete link lengths."""
    if not (0<=p<=1 and 0<low<=high):
        raise ValueError('Requires 0<=p<=1 and 0<low<=high')
    delta=high-low
    mean=low+p*delta
    variance=p*(1-p)*delta**2
    return dict(prob_high=p, mean_length=mean,variance=variance,
                rms_fluctuation=math.sqrt(variance),
                base888_factorization='C^888 = C^2 tensor C^444')


def two_link_fluctuations(p:float,low:float=1.,high:float=2.):
    """Quantum two-link Bell-like correlated state sqrt(1-p)|00>+sqrt(p)|11>.

    Length operator on each link is diagonal. This gives perfect positive
    covariance; an independent product state has zero covariance instead.
    """
    v=quantum_link(p,low,high)['variance']
    return dict(single_link_variance=v,
                two_independent_total_variance=2*v,
                two_entangled_total_variance=4*v,
                covariance_entangled=v)


def standard_model_anomalies():
    """Ordinary one-generation LEFT-handed Weyl multiplet, by assumption.

    Q_L (3,2) +1/6 ; u^c (3bar,1) -2/3 ; d^c (3bar,1) +1/3;
    L (1,2) -1/2 ; e^c (1,1) +1 ; nu^c (1,1) 0.
    """
    u1_cubed=(6*F(1,6)**3+3*F(-2,3)**3+3*F(1,3)**3
               +2*F(-1,2)**3+F(1)**3+F(0))
    mixed_gravity=(6*F(1,6)+3*F(-2,3)+3*F(1,3)+2*F(-1,2)+F(1))
    su2_sq_u1=(3*F(1,6)*F(1,2)+F(-1,2)*F(1,2))
    su3_sq_u1=(2*F(1,6)*F(1,2)+F(-2,3)*F(1,2)+F(1,3)*F(1,2))
    # Standard Model SU(3)^3 anomaly cancellation: 2 triplets - 1 anti-u - 1 anti-d = 0.
    su3_cube=2-1-1
    witten_doublets=4 # 3 coloured quark doublets plus 1 lepton doublet
    return {
        'U1_cubed':str(u1_cubed),'gravitational_U1':str(mixed_gravity),
        'SU2_squared_U1':str(su2_sq_u1),'SU3_squared_U1':str(su3_sq_u1),
        'SU3_cubed':str(su3_cube),'SU2_global_even_doublets':witten_doublets%2==0,
        'generations_assumed':3,
        'left_chiral_states_per_generation_with_nuR':16,
        'states_selected':48,
        'unused_888_dimension':840,
        'note':'These representations were assigned; no microscopic selection rule is derived.'
    }


def massive_memory_normal_modes(mphi:float,M:float,g:float):
    """Squared mass eigenvalues for two linearly mixed scalar fields."""
    if mphi<0 or M<0:raise ValueError('nonnegative masses required')
    discriminant=math.sqrt((mphi*mphi-M*M)**2+4*g*g)
    lo=(mphi*mphi+M*M-discriminant)/2
    hi=(mphi*mphi+M*M+discriminant)/2
    return {'omega_sq_minus':lo,'omega_sq_plus':hi,
            'linearly_stable':lo>=-1e-12}


def ccr_finite_dimension_obstruction(n:int=N):
    """The trace of [X,P] is zero, whereas Tr(i I_n)=i*n.

    Hence ||[X,P]-iI||_F >= sqrt(n) by the trace Cauchy-Schwarz bound.
    This is an exact algebraic impossibility theorem, not a numerical fit.
    """
    if n < 1: raise ValueError('Dimension must be positive')
    return {'dimension':n, 'commutator_trace':0,
            'imaginary_part_of_i_identity_trace':n,
            'frobenius_residual_lower_bound_hbar_1':math.sqrt(n),
            'exact_canonical_CCR_possible':False}


def effective_graviton_oscillator(k:float):
    """Known low-energy TT graviton oscillator *assuming* continuum GR.
    In natural units, a canonical Fourier oscillator has vacuum Var(q)=1/(2|k|).
    Does NOT show emergence of a graviton from Base888.
    """
    if k<=0:raise ValueError('nonzero momentum needed')
    return {'k':k,'omega':k,'vacuum_variance_q':1/(2*k),
            'count_TT_helicities':2,
            'status':'conditional continuum effective field theory, not derived from Base888'}


def report(tau=8.0,p=0.5):
    cyc=laplacian_cycle()
    tor=laplacian_torus()
    return {'model':'QST-002 exact candidate calculations',
      'source_states':N,
      'finite_CCR_obstruction':ccr_finite_dimension_obstruction(),
      'diffusion_time':tau,
      'ring_spectral_dimension':spectral_dimension(cyc,tau),
      'assumed_torus_shape':list(SHAPE_3),
      'assumed_torus_spectral_dimension':spectral_dimension(tor,tau),
      'quantum_link':quantum_link(p),
      'entanglement_correlations':two_link_fluctuations(p),
      'SM_anomaly_checks':standard_model_anomalies(),
      'memory_modes':massive_memory_normal_modes(1,2,0.25),
      'assumed_EFT_TT_mode':effective_graviton_oscillator(1),
      'scientific_status':'Mathematical toy checks only; no derived spacetime, SM or UV complete quantum gravity'}

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--tau',type=float,default=8.0)
    parser.add_argument('--p',type=float,default=.5)
    args=parser.parse_args()
    print(json.dumps(report(args.tau,args.p),indent=2))
