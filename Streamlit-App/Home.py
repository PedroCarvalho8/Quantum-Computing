import streamlit as st
import numpy as np
from sidebar import sidebar

sidebar()

# st.set_page_config(page_icon=":smile:")

st.title("Home")
st.write("Aplicativo dedicado à reunir problemas de computação quântica e exibilos de maneira interativa")

st.header("Problemas")
if st.button(":deciduous_tree: Eight Trees Problem", use_container_width=True):
    st.switch_page("pages/1-Eight_Trees_Problem.py")

if st.button(":bar_chart: New Mach", use_container_width=True):
    st.switch_page("pages/2-New_Mach.py")

if st.button(":speech_balloon: Superdense Coding", use_container_width=True):
    st.switch_page("pages/3-Superdense_Coding.py")
