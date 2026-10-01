from random import *
from math import sqrt
import math
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm
import numpy as np
from scipy.stats import norm, expon


class bernoulli:
    def _init_(self,nbpas,p):
        nbpas=nbpas
        p=p
    def bernoullifunction(self,p,nbpas):
   
        st=0
        sc=0
        for i in range(nbpas):
            t=random()<p # type: ignore
            st+=t
            sc+=t*t
        esp=(1/nbpas)*(st)
        var=sqrt((1/nbpas)*sc-(esp * esp))
        return esp,var
class uniforme:
    def __init__(self,nbpas):
        nbpas=nbpas
    def uniformefunction(self,nbpas):
        st=0
        sc=0
        for i in range(nbpas): # type: ignore
            t=random()
            st+=t
            sc+=t*t
        esp=(1/nbpas)*(st)
        var=sqrt((1/nbpas)*sc-(esp * esp))
        return esp,var
class exponentialloi:
    def __init__(self,lamda,nbpas):
        lamda=lamda
        nbpas=nbpas
    def exponentialfunction(self,lamda,nbpas):
        st=0
        sc=0
        for i in range(nbpas):
            t=math.log(1-random())
            t1=-(t)*(1/lamda)
            st=+t1
            sc=t*t
        esp=(1/nbpas)*(st)
        var=sqrt((1/nbpas)*sc-(esp * esp))
        return esp,var
class normalloi:
    def __init__(self,nbpas):
        nbpas=nbpas    
    def normalfunction1(self,nbpas,nbsimulation):
        for i in range(nbpas):
            t=sqrt(-2*math.log(random()))*math.cos(2*math.pi*random())
            st=+t
            sc=t*t
        esp=(1/nbpas)*(st)
        var=sqrt((1/nbpas)*sc-(esp*esp))
        return esp
    def normalfunction(self,nbpas,nbsimulation,seed=None):
        Pi=np.pi
        if seed is not None:
            np.random.seed(seed)
        np.random.seed(42)
        u1=np.random.uniform(0,1,(nbsimulation,nbpas))
        u2=np.random.uniform(0,1,(nbsimulation,nbpas))
        t=np.sqrt(-2*np.log(u1))*np.cos(2*Pi*u2)
        return t
class sousjacent:
    def __init__(self,nbpas,nbsimulation) :
        nbpas=int(nbpas)
        nbsimulation=int(nbsimulation)
    def sousjacentprice(self,r,sigma,T,S0,nbpas,nbsimulation,seed=None):
        
        St=np.zeros((nbsimulation,nbpas+1))
        St[:,0]=S0
        dt=T/nbpas
        b=normalloi(nbpas=nbpas)
        z=b.normalfunction(nbpas,nbsimulation,seed)
        for i in range(nbsimulation):
            S=S0
            for j in range(nbpas):
                S = S * math.exp((r - 0.5 * sigma**2) * dt+ sigma * math.sqrt(dt) * z[i, j])
                St[i,j+1]=S
        ST=St[:,-1]  
        return ST
class montécarlo:
    def primecallprix(self,sigma,S0,T,K,nbpas,r,nbsimulation,seed=None):
        v=sousjacent(nbsimulation=nbsimulation,nbpas=nbpas)
        ST=v.sousjacentprice(r,sigma,T,S0,nbpas,nbsimulation)
        payoffs=np.maximum(ST-K,0)
        #print(payoffs)
        v=np.mean(payoffs)
        c=np.exp((-r)*T)*v
        return c
    def primepuTprix(self,sigma,S0,T,K,nbpas,r,nbsimulation,seed=None):
        v=sousjacent(nbsimulation=nbsimulation,nbpas=nbpas)
        ST=v.sousjacentprice(r,sigma,T,S0,nbpas,nbsimulation)
        payoffs=np.maximum(K-ST,0)
        v=np.mean(payoffs)
        p=np.exp((-r)*T)*v
        #print(payoffs)
        return p
class blackandscholes:

    def primecallblackandscholes(self,sigma,T,S0,K,r):
        F = norm().cdf
        d1 = (math.log(S0 / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
        d2=d1-sigma*(math.sqrt(T))
        c=S0*F(d1)-K*math.exp((-r)*T)*F(d2)
        return c
    def primeputblackandscholes(self,sigma,T,S0,K,r):
        d1 = (math.log(S0 / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
        F1 = norm.cdf(-d1)
        d2=d1-sigma*math.sqrt(T)
        F2 = norm.cdf(-d2)
        p=K*math.exp((-r)*T)*F2-S0*F1
        return p
class reductiondevariance:
    
    """def pricingreductioncall(self,sigma,T,S0,K,r,nbpas,nbsimulation):
        t=normalloi(nbpas=nbpas)
        z=t.normalfunction(nbpas,nbsimulation)
        zreduit=-z
        St=np.zeros((nbsimulation,nbpas+1))
        St[0,:]=S0
        Streduit=np.zeros((nbsimulation,nbpas+1))
        Streduit[0,:]=S0
        dt=T/nbpas
        for i in range(nbsimulation):
            S=S0
            S1=S0
            for j in range(nbpas):
                S=S*math.exp((r-(sigma**2)*0.5)*(dt)+sigma*z[i,j]*math.sqrt(dt) )
                St[i,j+1]=S
                S1=S1*math.exp((r-(sigma**2)*0.5)*(dt)+sigma*zreduit[i,j]*math.sqrt(dt)) 
                Streduit[i,j+1]=S1
        ST=St[:,-1]
        STreduit=Streduit[:,-1]
        payoffs=np.maximum(ST-K,0)
        payoffsreduit=np.maximum(0,STreduit-K)
        CT=np.mean((0.5*(payoffs+payoffsreduit)))*np.exp((-r)*T)
        return CT
    def pricingreductionpuT(self,sigma,T,S0,K,r,nbpas,nbsimulation):
        t=normalloi(nbpas=nbpas)
        z=t.normalfunction(nbpas,nbsimulation)
        zreduit=-z
        St=np.zeros((nbsimulation,nbpas+1))
        Streduit=np.zeros((nbsimulation,nbpas+1))
        St[:,0]=S0
        Streduit[:,0]=S0
        dt=T/nbpas
        for i in range(nbsimulation):
            S=S0
            S1=S0
            for j in range(nbpas):
                S=(S*math.exp((r-(sigma**2)*0.5)*(dt)+sigma*z[i,j]*math.sqrt(dt) ))
                St[i,j+1]=S
                S1=(S1*math.exp((r-(sigma**2)*0.5)*(dt)+sigma*zreduit[i,j]*math.sqrt(dt) ))
                Streduit[i,j+1]=S1
        ST=St[:,-1]
        STreduit=Streduit[:,-1]
        payoffs=np.maximum(K-ST,0)
        payoffsreduit=np.maximum(0,K-STreduit)
        PT=np.mean((0.5*(payoffs+payoffsreduit)))*np.exp((-r)*T)
        return PT"""
    def pricingreductioncall(self, sigma, T, S0, K, r, nbpas, nbsimulation,seed=None):

        t = normalloi(nbpas=nbpas)
        z = t.normalfunction(nbpas, nbsimulation)   
        zreduit = -z

        dt = T / nbpas

        St = np.zeros((nbsimulation, nbpas + 1))
        Streduit = np.zeros((nbsimulation, nbpas + 1))

        St[:, 0] = S0
        Streduit[:, 0] = S0
        for i in range(nbsimulation):
            for j in range(nbpas):
                St[i, j+1] = St[i, j] * math.exp(
                    (r - 0.5 * sigma**2) * dt + sigma * math.sqrt(dt) * z[i, j]
                )
                Streduit[i, j+1] = Streduit[i, j] * math.exp(
                    (r - 0.5 * sigma**2) * dt + sigma * math.sqrt(dt) * zreduit[i, j]
                )

        ST = St[:, -1]
        STreduit = Streduit[:, -1]

        payoffs = np.maximum(ST - K, 0)
        payoffsreduit = np.maximum(STreduit - K, 0)

        CT = 0.5 * (np.exp(-r*T) * np.mean(payoffs) +np.exp(-r*T) * np.mean(payoffsreduit))

        return CT
    

    def pricingreductionput(self, sigma, T, S0, K, r, nbpas, nbsimulation,seed=None):

        t = normalloi(nbpas=nbpas)
        z = t.normalfunction(nbpas, nbsimulation)
        zreduit = -z

        dt = T / nbpas

        St = np.zeros((nbsimulation, nbpas + 1))
        Streduit = np.zeros((nbsimulation, nbpas + 1))

        St[:, 0] = S0
        Streduit[:, 0] = S0

        for i in range(nbsimulation):
            for j in range(nbpas):
                St[i, j+1] = St[i, j] * math.exp(
                    (r - 0.5 * sigma**2) * dt + sigma * math.sqrt(dt) * z[i, j]
                )
                Streduit[i, j+1] = Streduit[i, j] * math.exp(
                    (r - 0.5 * sigma**2) * dt + sigma * math.sqrt(dt) * zreduit[i, j]
                )

        ST = St[:, -1]
        STreduit = Streduit[:, -1]

        payoffs = np.maximum(K - ST, 0)
        payoffsreduit = np.maximum(K - STreduit, 0)

        PT= 0.5 * (np.exp(-r*T) * np.mean(payoffs) +np.exp(-r*T) * np.mean(payoffsreduit))


        return PT
v=sousjacent(nbpas=30,nbsimulation=30)
r=0.9 
sigma=0.2
T=1
S0=20
nbpas=30
nbsimulation=30
#t = np.linspace(0, T, nbpas )
"""ST=v.sousjacentprice(r,sigma,T,S0,nbpas,nbsimulation)
for i in range(nbpas):
    plt.plot(St[i])
plt.title('variation du cours su sous-jacent dans le temps')
plt.xlabel('temps')
plt.ylabel('cours')
plt.grid()
plt.show()"""
    
       

"""fig2, ax2 = plt.subplots(figsize=(8, 4))
ax2.hist(ST, bins=30, alpha=0.7)
ax2.set_xlabel("Prix `a maturit´e")
ax2.set_ylabel("Fr´equence")
plt.show() """              
