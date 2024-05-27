import streamlit as st
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import cmath
import math
simulador = AerSimulator()

def probabilidade(entrada, ket):
    return np.power(np.absolute(np.matmul(ket, entrada)), 2)

def beam_splitter(r):
    T = cmath.sqrt(1 - np.power(r, 2)) 
    return np.array([[r, T],[T ,-r]])           

def mz_interferometer(r):
    ket0 = np.array([1, 0])
    ket1 = np.array([0, 1])

    U = beam_splitter(r)                   
    saida_primeiro_splitter = np.matmul(U, ket0)
    saida_segundo_splitter = np.matmul(U, ket1)
    
    A = probabilidade(saida_primeiro_splitter, ket0)
    B = probabilidade(saida_primeiro_splitter, ket1) * probabilidade(saida_segundo_splitter, ket1)
    C = probabilidade(saida_primeiro_splitter, ket1) * probabilidade(saida_segundo_splitter, ket0)

    return np.array([B, A + C])

def print_matrix(array):
    matrix = ''
    for row in array:
        try:
            for number in row:
                matrix += f'{number}&'
        except TypeError:
            matrix += f'{row}&'
        matrix = matrix[:-1] + r'\\'
    st.latex((r'\begin{bmatrix}'+matrix+r'\end{bmatrix}'))

def string_to_bin(mensagem):
    bytes = mensagem.encode('utf-8')
    binario = ''.join(format(byte, '08b') for byte in bytes)
    binarios = []
    for i in range (len(binario)):
        binarios.append(int(binario[i]))
    return binarios

def bin_to_string(bin):
    bytes = int(bin, 2).to_bytes((len(bin) + 7) // 8, byteorder='big')
    string = bytes.decode('utf-8')
    return string


def protocol(binarios):
    binarios_medidos = []

    for i in range(0, int(len(binarios)), 2):
        circEmaranhado = emaranhar(2)
        bits_a_enviar = [binarios[i], binarios[i+1]]
        circEncode = sua_parte(circEmaranhado, bits_a_enviar)
        bits_recebidos = alice_parte(circEncode)
        for i in range(2):
            binarios_medidos.append(bits_recebidos[i])
    
    return binarios_medidos


def emaranhar(qubits):
    qc = QuantumCircuit(qubits, qubits)
    qc.h(0)
    qc.cx(0, 1)
    qc.barrier()
    return qc

def sua_parte(qc, bin):
    match bin:
       case [0, 0]:
            qc.id(0)
        case [0, 1]:
            qc.z(0)
        case [1, 0]:
            qc.x(0)
        case [1, 1]:
            qc.x(0)
            qc.z(0)
    
    qc.barrier()

    return qc

def alice_parte(qc):
    qc.cx(0,1)
    qc.h(0)
    qc.measure([0, 1], [0, 1])

    bin = simulador.run(qc, shots = 1).result().get_counts()

    return [int(list(bin.keys())[0][0]), int(list(bin.keys())[0][1]), qc]
