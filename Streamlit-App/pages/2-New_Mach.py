import streamlit as st
import pandas as pd
import numpy as np
import cmath
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator
from quantica import mz_interferometer, print_matrix, beam_splitter
from sidebar import sidebar


st.set_page_config(page_title="New Mach")

sidebar()

st.title('''New Mach''')

st.link_button("Problema no GitHub", "https://github.com/PedroCarvalho8/Quantum-Computing/tree/main/New-Mach")

st.header('''Alterar valores''')
r = st.slider("Valor do raio do beam splitter: ", 0.0, 1.0, 0.5)
interferometro = mz_interferometer(r)

dados = [[interferometro[0], interferometro[1]]]
df = pd.DataFrame(data = dados)
df = df.rename({0: 'Probabilidade B', 1: 'Probabilidade A ou C'}, axis='columns')

st.header('''Matriz representando o beam splitter''')
T = np.round(cmath.sqrt(1 - np.power(r, 2)), 4)
print_matrix([[r, T], [T, -r]])


st.header('''Tabela probabilidades''')
st.write(df)

st.header('''Circuito''')

U = beam_splitter(r)    
qc = QuantumCircuit(1, 1)

qc.unitary(U, 0, label = "Beam Splitter")
qc.measure(0, 0)
qc.unitary(U, 0, label = "Beam Splitter").c_if(0, val = 1)
qc.measure(0, 0)

from streamlit_javascript import st_javascript
st_theme = st_javascript("""window.getComputedStyle(window.parent.document.getElementsByClassName("stApp")[0]).getPropertyValue("color-scheme")""")

style_dark = {"backgroundcolor": "#0e1117",
         "textcolor": "white",
         "linecolor": "white",
         "displaycolor": {
             "unitary": ["#fa4b4b", "white"]}}

style_light = {
         "displaycolor": {
             "unitary": ["#fa4b4b", "white"]}}

st.write(qc.draw(output="mpl", style = (st_theme == 'dark' and style_dark or style_light)))

