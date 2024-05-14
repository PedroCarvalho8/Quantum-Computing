import streamlit as st
from quantica import protocol, bin_to_string, string_to_bin, emaranhar, alice_parte, sua_parte
from sidebar import sidebar

tab_main, tab_converter = st.tabs(["Superdense Coding", "Converter binários"])

sidebar()

from streamlit_javascript import st_javascript
st_theme = st_javascript("""window.getComputedStyle(window.parent.document.getElementsByClassName("stApp")[0]).getPropertyValue("color-scheme")""")

with tab_main:
    st.title("Superdense Coding")

    st.link_button("Problema no GitHub", "https://github.com/PedroCarvalho8/Quantum-Computing/tree/main/Superdense-Coding")

    style_dark = {"backgroundcolor": "#0e1117",
         "textcolor": "white",
         "linecolor": "white",
         "displaycolor": {
             "unitary": ["#fa4b4b", "white"]}}
    style_light = {
         "displaycolor": {
             "unitary": ["#fa4b4b", "white"]}}

    if 'passar_emaranhamento' not in st.session_state:
        st.session_state['passar_emaranhamento'] = False

    if 'passar_encode' not in st.session_state:
        st.session_state['passar_encode'] = False

    if 'passar_decode' not in st.session_state:
        st.session_state['passar_decode'] = False

    if 'passar_medir' not in st.session_state:
        st.session_state['passar_medir'] = False

    col1, col2 = st.columns(2)
    bit1 = col1.number_input("bit 1:", min_value=0, max_value=1, disabled=st.session_state['passar_emaranhamento'])
    bit2 = col2.number_input("bit 2:", min_value=0, max_value=1, disabled=st.session_state['passar_emaranhamento'])
    if not st.session_state['passar_emaranhamento']:
        if st.button("Emaranhar bits", use_container_width=True):
            st.session_state['passar_emaranhamento'] = True
            st.rerun()
    if  st.session_state['passar_emaranhamento']:

        
        st.session_state['passar_emaranhamento'] = True
        st.header("Emaranhamento")
        circuito = emaranhar(2)
        st.write(circuito.draw(output="mpl", style = (st_theme == 'dark' and style_dark or style_light)))
        if not st.session_state['passar_encode']:
            if st.button("Encode", use_container_width=True):
                st.session_state['passar_encode'] = True
                st.rerun()
        if  st.session_state['passar_encode']:

            st.header("Encode")
            circuito = sua_parte(circuito, [int(bit1), int(bit2)])
            st.write(circuito.draw(output="mpl", style = (st_theme == 'dark' and style_dark or style_light)))
            if not st.session_state['passar_decode']:
                if st.button("Decode", use_container_width=True):
                    st.session_state['passar_decode'] = True
                    st.rerun()
            if  st.session_state['passar_decode']:

                st.header("Decode")
                medidas = alice_parte(circuito)
                circuito = medidas[2]
                st.write(circuito.draw(output="mpl", style = (st_theme == 'dark' and style_dark or style_light)))
                if not st.session_state['passar_medir']:
                    if st.button("Medir", use_container_width=True):
                        st.session_state['passar_medir'] = True
                        st.rerun()
                if  st.session_state['passar_medir']:
                    st.header("Medição")
                    st.write("Bits medidos: ", medidas[0], medidas[1])

    if st.button("Resetar", help="Clique para resetar o protocolo"):
        st.session_state['passar_emaranhamento'] = False
        st.session_state['passar_encode'] = False
        st.session_state['passar_decode'] = False
        st.session_state['passar_medir'] = False
        st.rerun()

 

with tab_converter: 
    st.title("Converter binários")
    st.header("Converter mensagem para binário")
    mensagem = st.text_input("Mensagem")
    if mensagem != "":
        mensagem_binario = string_to_bin(mensagem)
        locais_para_inserir = []
        for i in range(len(mensagem_binario)):
            if ((i+1)%8 == 0):
                locais_para_inserir.append(i+1)
        continuar = True
        n = 0
        while n != (len(locais_para_inserir)):
            mensagem_binario.insert(locais_para_inserir[n]+n, " ")
            n+=1

        mensagem_binario_str = ''.join(str(x) for x in mensagem_binario)
        binario_a = mensagem_binario
        st.subheader("Mensagem em binário:")
        st.write(mensagem_binario_str)

    st.header("Converter binário para texto")


    activated = st.toggle("Converter manualmente", value = True)

    if activated:
        binario = st.text_input("Binário")
        if st.button("Converter binário", use_container_width=True):
            binario = binario.split(" ")
            binario = "". join(binario)
            if binario != "" and len(binario)%8 == 0:
                parar = False
                bins = ['0', '1']
                for i in range (len(binario)):
                    if binario[i] not in bins:
                        parar = True
                if not parar:
                    st.subheader("Binário convertido para texto:")
                    bin_string = bin_to_string(binario)
                    st.write(bin_to_string(binario))
                else:
                    st.error('Erro, insira um binário válido', icon="🚨")
            else:
                st.error('Erro, insira um binário válido', icon="🚨")
    else:
        opcoes_msg = ["", None]
        if mensagem not in opcoes_msg:
            binario = mensagem_binario_str
            binario = binario.split(" ")
            binario = "". join(binario)
            st.subheader("Binário convertido para texto:")
            bin_string = bin_to_string(binario)
            st.write(bin_to_string(binario))

# with col1:   
#     bit1 = st.number_input("bit 1", max_value=1, min_value=0)
# with col2:
#     bit2 = st.number_input("bit 2", max_value=1, min_value=0)

# bits = [bit1, bit2]

# if st.button("Enviar bits"):
#     st.write(bits)

# if mensagem!= "":
#     binarios_enviados = protocol(string_to_bin(mensagem)) # Realiza todo o protocolo a partir dos binarios equivalente à mensagem
#     binarios_convertidos = ''.join(str(x) for x in binarios_enviados) # Converte a lista de binario para uma string de binarios
#     mesangem_decodificada = bin_to_string(binarios_convertidos) # Decodifica os binarios
    
#     # Exibe a mensagem decodificada
#     st.write("Mensagem recebida: " + mesangem_decodificada)

#     # Verifica se a mensagem decodificada equivale à mensagem enviada
#     st.write("Os binários recebidos são iguais aos enviados?", binarios_enviados == string_to_bin(mensagem)) 