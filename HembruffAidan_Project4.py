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
    return (np.exp((-((xi-x0)**2))/(2*(sigma0**2))))*(np.exp(1j*k0*xi))/np.sqrt(sigma0*np.sqrt(np.pi)) # wavepacket function equation 9.42

def sch_eqn(nspace,ntime,tau,method="ftcs",length=200,potential=[],wparam=[10,0,0.5]):
    """
    

    Parameters
    ----------
    nspace : TYPE
        DESCRIPTION.
    ntime : TYPE
        DESCRIPTION.
    tau : TYPE
        DESCRIPTION.
    method : TYPE, optional
        DESCRIPTION. The default is "ftcs".
    length : TYPE, optional
        DESCRIPTION. The default is 200.
    potential : TYPE, optional
        DESCRIPTION. The default is [].
    wparam : TYPE, optional
        DESCRIPTION. The default is [10,0,0.5].

    Returns
    -------
    psi : TYPE
        DESCRIPTION.
    x : TYPE
        DESCRIPTION.
    t : TYPE
        DESCRIPTION.
    probability : TYPE
        DESCRIPTION.

    """
    
    sigma0 , x0, k0 =  wparam[0], wparam[1], wparam[2] 
    h = length/(nspace-1)
    
    hbar = 1
    mass = 0.5
    ftcs_coeff = 1j*tau/hbar 
    
    crank_coeff = 1j*tau/(2*hbar)
    
    H_coeff = -hbar**2/(2*mass*h)
    
    H = H_coeff*make_tridiagonal(nspace,1,-2,1)
    
    # Periodic BCs from Textbook
    H[0,-1] = H_coeff ; H[0,0] = -2*H_coeff ; H[0,1] = H_coeff
    H[-1,2] = H_coeff ; H[-1,-1] = -2*H_coeff ; H[-1,0] = H_coeff
    
    if len(potential) != 0:
        for i in potential:
            H[i,i] += 1  
    
    x = np.linspace(-length/2,length/2,nspace)
    t = tau*np.arange(0,ntime) # the time grid
    
    if method == "ftcs":
        
        probability = np.zeros((ntime))
        
        # below from Lab 11
        psi = np.zeros((nspace,ntime),dtype=complex) # initialize the array for storing the complete spatial solution
        
        # initial condition using make_initialcond function developed in Lab 10
        psi[:,0] = make_initialcond(x,k0,sigma0,x0)
        
        ftcs_A = np.identity(nspace,dtype=complex) - ftcs_coeff*H
        
        # following 7 lines adapted from Lab 11
        # iterate over the number of time steps to obtain spatial solutions for every time step
        for istep in range(1, ntime):
            psi[:,istep] = ftcs_A.dot(psi[:,istep-1])
            
            #probability[istep] = psi[:,istep]*(np.conjugate(psi[:,istep]))
            
        
        # Solution stability is determined by maximum valued eigenvalue of A
        # spectral_radius function is from Lab 10
        stability = spectral_radius(ftcs_A)
        
        # print statement for solution stability
        if stability <= 1:
            print("Solution is expected to be stable")
        else:
            print("Warning! Solution is expected to be unstable")
            
    if method == "crank":
        
        probability = np.zeros((ntime))
        
        psi = np.zeros((nspace,ntime),dtype=complex)
        
        # initial condition using make_initialcond function developed in Lab 10
        psi[:,0] = make_initialcond(x,k0,sigma0,x0)
        
        crank_A = np.dot(inv(np.identity(nspace,dtype=complex)+crank_coeff*H),(np.identity(nspace,dtype=complex)-crank_coeff*H))
        
        # following 7 lines adapted from Lab 11
        # iterate over the number of time steps to obtain spatial solutions for every time step
        for istep in range(1, ntime):
            psi[:,istep] = np.dot(crank_A,psi[:,istep-1])
            
            # integrate over the grid length?
            #probability[istep] = psi[:,istep]*(np.conjugate(psi[:,istep]))
    
    return psi, x, t, #probability

sol = sch_eqn(80,200,1,"crank")
x =  sol[1]
psi = sol[0]
index = 0


def sch_plot(plot_type="psi",save=True,filepath="HembruffAidan_Project4_Fig1.png"):
    """
    

    Parameters
    ----------
    plot_type : TYPE, optional
        DESCRIPTION. The default is "psi".
    save : TYPE, optional
        DESCRIPTION. The default is True.
    filepath : TYPE, optional
        DESCRIPTION. The default is "HembruffAidan_Project4_Fig1.png".

    Returns
    -------
    None.

    """
    
    fig = plt.figure()
        
    if plot_type == "psi":
        # adapted from textbook
        plt.plot(x, np.real(psi[:,index]))
        plt.xlabel("x") ; plt.ylabel(r"$\psi(x)$")
        plt.title("Real Wavefunction")
        plt.show()
    
    if plot_type == "prob":
        density = psi[:,index]*np.conjugate(psi[:,index])
        plt.plot(x, density)
        plt.xlabel("x") ; plt.ylabel("P(x,t)")
        plt.title("Probability Density")
        plt.show()
        
    if save == True:
        plt.savefig(filepath)
    
    return

sch_plot(plot_type="prob",save=False)

# END
