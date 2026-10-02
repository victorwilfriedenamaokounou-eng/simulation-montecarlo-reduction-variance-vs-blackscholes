import pandas as pd
import streamlit as st
from pricing import bernoulli
from pricing import uniforme
from pricing import exponentialloi
from pricing import normalloi
from pricing  import sousjacent
from pricing import montécarlo
from pricing import blackandscholes
from pricing import reductiondevariance

st.title('pricing option interface')
st.write('voulez pricer une option ou alors simuler une loi')
sigma=st.number_input('entrez la volatilité')
T=st.number_input('entrez la maturité T')
nbsimulation=st.number_input('entrez le nombre de simulation',min_value=10,max_value=10000,step=1)
r=st.number_input('entrez le taux sans risque',step=0.001 )
nbpas=int(st.number_input('entrez le nombre de chemin que vous voulez simuler',min_value=1,max_value=10000,step=1))
S0=st.number_input('entrez le prix actuel du sous-jacent')
K=st.number_input('le prx d exercice de l option')
if S0!=0 and nbpas!=0 and r!=0 and T!=0 and sigma!=0:
    v=montécarlo()
    w=blackandscholes()
    t=reductiondevariance()
    st.button(" call",type='primary')
    st.button(" puT",type='primary')
    st.button("réductiondevariance",type='primary')
    if st.button("call"):
        prixcall=v.primecallprix(sigma,S0,T,K,nbpas,r,nbsimulation)
        st.write("le prix par la méthode de monté carlo est:",prixcall)
        prixblackandscholes=w.primecallblackandscholes(sigma,T,S0,K,r)
        st.write("le prix black and scholes est",prixblackandscholes)
    if st.button("PuT"):
        prixput=v.primepuTprix(sigma,S0,T,K,nbpas,r,nbsimulation)
        st.write("le prix puT monté carlo est :",prixput)
        blackandscholesput=w.primeputblackandscholes(sigma,T,S0,K,r)
        st.write("le prix put black and scholes est:",blackandscholesput)    
    if st.button("reductiondevariance"):
            prixput=t.pricingreductionput(sigma,T,S0,K,r,nbpas,nbsimulation)
            st.write('le prix réduction de variance:',prixput)
            prixput=v.primepuTprix(sigma,S0,T,K,nbpas,r,nbsimulation)
            st.write("le prix puT monté carlo est :",prixput)
            blackandscholesput=w.primeputblackandscholes(sigma,T,S0,K,r)
            st.write("le prix put black and scholes est:",blackandscholesput)
            prixcall=t.pricingreductioncall(sigma,T,S0,K,r,nbpas,nbsimulation)
            st.write('le prix réduction de variance est de:',prixcall)
            prixcall=v.primecallprix(sigma,S0,T,K,nbpas,r,nbsimulation)
            st.write("le prix par la méthode de monté carlo est de:",prixcall)
            prixblackandscholes=w.primecallblackandscholes(sigma,T,S0,K,r)
            st.write("le prix black and scholes est de",prixblackandscholes)