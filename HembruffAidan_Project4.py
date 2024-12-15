# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 13:57:24 2024

@author: aidan
"""

# Project 4

import numpy as np
from numpy.linalg import eig
from numpy.linalg import inv
import cmath
import matplotlib.pyplot as plt

def spectral_radius(A):
    '''
    Author : Aidan Hembruff
    
    **This function was originally developed in and is completely adapted from Lab 10
    
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

def make_tridiagonal(N,b,d,a):
    '''
    Author : Aidan Hembruff
    
    **This function was originally developed in and is completely adapted from Lab 10
    
    A function which takes numerical inputs to generate an NxN
    tridiagnonal matrix with specified values

    Parameters
    ----------
    N : The length of the array's rows and columns
    
    b : The value which will go on the lower diagonal
    
    d : The value which will go on the main diagonal
    
    a : The value which will go on the upper diagonal

    Returns
    -------
    The tridiagonal matrix generated by the input values

    '''
    # create the tridiagonal matrix by summing matrices with the specified values,
    # on the lower, main, and upper diagonals
    return d*np.identity(N,dtype=complex)+(b*np.eye(N,k=-1,dtype=complex))+(a*np.eye(N,k=1,dtype=complex)) 

def make_initialcond(xi,k0,sigma0,x0):
    '''
    Author : Aidan Hembruff
    
    **This function was originally developed in Lab 10 and has been modified for the 
    purposes of this project.
    
    A function which returns the normalized initial wavepacket of a given form
    based on scalable input parameters and grid 
    
    Parameters
    ----------
    xi : The spatial grid which the wavepacket will be a function of
    
    k0 : Scalable parameter for the wavepacket (wavenumber)
    
    sigma0 : Scalable parameter for the wavepacket (standard deviation)
    
    x0 : The initial position of the wavepacket on the grid

    Returns
    -------
    The normalized wavepacket function determined by the parameters and spatial grid

    '''
            # wavepacket function given in equation 9.42 of NM4P
    return (np.exp((-((xi-x0)**2))/(2*(sigma0**2))))*(np.exp(1j*k0*xi))/np.sqrt(sigma0*np.sqrt(np.pi)) 

def sch_eqn(nspace,ntime,tau,method="ftcs",length=200,potential=[],wparam=[10,0,0.5]):
    """
    Author : Aidan Hembruff
    
    A function to numerically solve the one dimensional, time-dependent Schrodinger equation
    using one of two methods : FTCS Explicit or Crank-Nicholson

    Parameters
    ----------
    nspace : The number of spatial grid points to solve the Schrodinger equation on
    
    ntime : The number of time steps over which the chosen method will be iterated
    
    tau : The size of the time step
    
    method : The chosen method by which the solution will be obtained. Either "ftcs"
    or "crank". The default is "ftcs"
    
    length : The length of the x-grid. The default is 200
        
    potential : The indices on the spatial grid at which the potential
    will be set to equal 1. The default is no positions, an empty array [] 
        
    wparam : The parameters for the initial wavepacket given in the form
    [sigma,k0,x0]. The default is [10,0,0.5]

    Returns
    -------
    psi : The two-dimensional array containing the complete spatial solution
    for the Schrodinger equation at every time interval
    
    x : The spatial grid on which the solution to the Schrodinger equation was calculated
    
    t : The time grid over which the solution to the Schrodinger equation was calculated
    
    probability : The one-dimensional array storing the conserved probability at
    each time step

    """
    # unpack parameters for the initial wavepacket
    sigma0 , x0, k0 =  wparam[0], wparam[1], wparam[2] 
    
    # defining parameters and coefficients
    h = length/(nspace-1)           # Grid spacing for a solution with periodic boundary conditions
    hbar = 1                        # The value of Planck's constant (divided by 2*pi) given in instructions
    mass = 0.5                      # The value for mass given in instructions
    
    # matrix coefficients given by NM4P Chapter 9 
    ftcs_coeff = 1j*tau/hbar        # Coefficient for the matrix used in the explicit ftcs scheme  (eq 9.32)
    crank_coeff = 1j*tau/(2*hbar)   # Coefficient for the matrix used in the Crank-Nicholson scheme (eq 9.40)
    H_coeff = -(hbar**2)/(2*mass*(h**2))   # Coefficient for the discretized Hamiltonian operator (schro program pp240)
    
    # constructing the Hamiltonian matrix using the make_tridiagonal function
    H = H_coeff*(np.identity(nspace)+make_tridiagonal(nspace,1,-2,1))
    
    # periodic boundary conditions given in the Schro program from NM4P
    H[0,-1] = H_coeff
    H[-1,0] = H_coeff
    H[0,1] = H_coeff
    H[-1,-2] = H_coeff
        
    if len(potential) != 0: # if potential array is not empty, run the following
        # add one to each diagonal element of the Hamiltonian matrix corresponding
        # to the given index
        for i in potential:
            H[i,i] += 1  
    
    # one-dimensional arrays to be returned by the function
    x = np.linspace(-length/2,length/2,nspace) # the spatial grid
    t = tau*np.arange(0,ntime) # the time grid
    
    # initialize the array for storing the total probability at every time step
    probability = np.zeros((ntime))
    
    # initialize the array for storing the complete spatial solution at every time step
    psi = np.zeros((nspace,ntime),dtype=complex) 
    
    # initial condition using make_initialcond function and given parameters
    psi[:,0] = make_initialcond(x,k0,sigma0,x0)
    
    # set the total probability of the initial condition
    probability[0] = np.sum(np.abs(psi[:,0]*np.conjugate(psi[:,0])))
    
    # run the Explicit FTCS scheme
    if method == "ftcs":
        
        # the matrix used for the explicit ftcs scheme
        ftcs_A = np.identity(nspace,dtype=complex) - ftcs_coeff*H
        
        # iterate over all time steps to obtain spatial solutions for every step
        for istep in range(0, ntime-1):
            # present spatial solution is determined by dot product of previous spatial
            # solution with the explicit FTCS scheme matrix
            # equation 9.32 from NM4P
            psi[:,istep+1] = ftcs_A.dot(psi[:,istep])
            
            # computing the current element probability array
            probability[istep+1] = np.sum(np.abs(psi[:,istep]*np.conjugate(psi[:,istep])))
            
        # Solution stability for explicit FTCS is determined by spectral_radius function
        stability = spectral_radius(ftcs_A)
        
        # print statement for solution stability
        if stability <= 1:
            print("Solution is expected to be stable")
        else:
            print("Warning! Solution is expected to be unstable")
        
    # run the Crank-Nicholson scheme
    if method == "crank":

        # the matrix for the Crank-Nicholson scheme        
        crank_A = np.dot(inv(np.identity(nspace,dtype=complex)+crank_coeff*H),(np.identity(nspace,dtype=complex)-crank_coeff*H))
        
        # iterate over all time steps to obtain spatial solutions for every step
        for istep in range(1, ntime):
            # present spatial solution is determined by dot product of previous spatial
            # solution with the Crank-Nicholson scheme matrix
            psi[:,istep] = np.dot(crank_A,psi[:,istep-1])
            
            # computing the probability array
            probability[istep] = np.sum(np.abs(psi[:,istep]*np.conjugate(psi[:,istep])))
    
    return psi, x, t, probability


def sch_plot(x,psi,time,plot_type="psi",save=True,filepath="HembruffAidan_Project4_Fig1.png"):
    """
    Author : Aidan Hembruff
    
    A function which plots the output of the sch_eqn function at a given time, either the
    real part of the spatial solution or the probability density as a function of x

    Parameters
    ----------
    x : The one-dimensional spatial grid on which the solution was calculated
    
    psi : The two-dimensional array containing the complete spatial solution of the 
    Schrodinger equation at every time step
    
    time : The time index in the psi array for which the plot will show the spatial solution
    
    plot_type : The type of plot to create, either "psi" - the real part of the wavefunction -
    or "prob" - the probability density. The default is "psi"
    
    save : Condition for saving the plot to a png file. The default is True
    
    filepath : The filepath to save the figure of the plot to.
    The default is "HembruffAidan_Project4_Fig1.png"
        
    Output
    ----------
    The desired plot and a saved figure (only if save condition is True)

    """
    
    # plot the real part of the wavefunction
    if plot_type == "psi":
        # adapted from NM4P "schro" program
        plt.plot(x, np.real(psi[:,time]))
        plt.xlabel("x") ; plt.ylabel(r"$\psi(x)$")
        plt.title("Real Wavefunction")
        plt.grid(True)
        plt.show()
    
    # plot the probability density
    if plot_type == "prob":
        density = np.abs(psi[:,time]*np.conjugate(psi[:,time]))
        plt.plot(x, density)
        plt.xlabel("x") ; plt.ylabel("P(x,t)")
        plt.title("Probability Density")
        plt.grid(True)
        plt.show()
    
    # save the figure if desired
    if save == True:
        plt.savefig(filepath)
        
    return


