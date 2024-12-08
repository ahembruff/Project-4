# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 13:57:24 2024

@author: aidan
"""

# Project 4

import numpy as np
from numpy.linalg import eig

def spectral_radius(A):
    '''
    Author : Aidan Hembruff
    
    A function which finds the eigenvalue with the maximum
    absolute value for a 2-D array

    Parameters
    ----------
    A : The input 2-dimensional matrix

    Returns
    -------
    The eigenvalue of the matrix with the maximum absolute value

    '''
    eigenvalues = eig(A)[0] # eigenvalues of A
    return np.max(np.abs(eigenvalues)) # maximum absolute eigenvalue

def make_initialcond(xi,k0,sigma0):
    '''
    Author : Aidan Hembruff
    
    A function which returns the initial wavepacket of a given form
    based on scalable input parameters and grid
    
    Parameters
    ----------
    xi : The spatial grid which the wavepacket will be a function of
    
    k0 : Scalable parameter for the wavepacket
    
    sigma0 : Scalable parameter for the wavepacket

    Returns
    -------
    The wavepacket function determined by the parameters and spatial grid

    '''
    return (np.exp((-(xi**2))/(2*(sigma0**2))))*np.cos(k0*xi) # wavepacket function

def sch_eqn(nspace,ntime,method="ftcs",lenght=200,potential=[],wparam=[10,0,0.5]):
    
    return

def sch_plot(plot_type,save=True):
    
    return