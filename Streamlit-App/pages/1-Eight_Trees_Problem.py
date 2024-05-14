import streamlit as st
from sidebar import sidebar
from qiskit import QuantumCircuit, QuantumRegister
import random

st.title("Eight Trees Problem")

st.link_button("Problema no GitHub", "https://github.com/PedroCarvalho8/Quantum-Computing/tree/main/Number-of-sets-is-odd")

sidebar()


st.header("Alterar valores")

col1, col2 = st.columns(2)

with col1:
    arvoresq = st.slider("Quantidade de árvores: ", 0, 6, value=3)

with col2:
    pedrasq = st.slider("Quantidade de pedras: ", 0, 6, value=3)
    
opcoes = [x for x in range(arvoresq+pedrasq)]

index_arvores_pedras = []
for x in range(arvoresq):
    escolha = random.choice(opcoes)
    index_arvores_pedras.append(escolha)
    opcoes.remove(escolha)
    
arvores = []    
for i in range(arvoresq+pedrasq):
    if i not in index_arvores_pedras:
        arvores.append(0)
    else:
        arvores.append(1)


qnt_espacos = len(arvores) 

qreg_q = QuantumRegister(qnt_espacos+1, 'q')
global circuit
circuit = QuantumCircuit(qreg_q)

        

for i in range(0, qnt_espacos): 
    if arvores[i] == 1: 
        circuit.x(qreg_q[i])
     
for i in range (0, qnt_espacos):
    circuit.cx(qreg_q[i], qreg_q[qnt_espacos])

for i in range (0, qnt_espacos-1):
    circuit.ccx(qreg_q[i], qreg_q[i+1], qreg_q[qnt_espacos])

from streamlit_javascript import st_javascript
st_theme = st_javascript("""window.getComputedStyle(window.parent.document.getElementsByClassName("stApp")[0]).getPropertyValue("color-scheme")""")

style_dark = {"backgroundcolor": "#0e1117",
         "textcolor": "white",
         "linecolor": "white",
         "displaycolor": {
             "x": ["green", "white"],
             "ccx": ["#fa4b4b", "white"],
             "cx": ["#fa4b4b", "white"]
         }}

style_light = {
         "displaycolor": {
             "x": ["green", "white"],
             "ccx": ["#fa4b4b", "white"],
             "cx": ["#fa4b4b", "white"]
         }}

st.header("Circuito")
st.write(circuit.draw(output="mpl", style = (st_theme == 'dark' and style_dark or style_light)))

circuit.measure_all()

from qiskit_aer import AerSimulator
simulador = AerSimulator()

resultado = list(simulador.run(circuit, shots = 1).result().get_counts(circuit).keys())[0][0]

st.header("Resultados")

def printar():
    lista = []
    for i in arvores:
        if i == 1:
            lista.append(":deciduous_tree:")
        else:
            lista.append(":rock:")
    return ''.join(lista)
st.markdown(f"A quantidade de conjustos de árvores é **{int(resultado)==0 and "Par" or "Ímpar"}**")
st.markdown(f"Representação do problema: {printar()}")