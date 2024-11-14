import streamlit as st
from groq import Groq
#CONFIGURANDO VENTANA WEB: modelos

MODELOS = ['llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768']

def crear_usuario_groq():
    clave_secreta = st.secrets["CLAVE_API"]
    return Groq(api_key = clave_secreta)

# CAMBIA EL STREAM A TRUEEE, NO TE OLVIDÉS, CUANDO PRENDÁS LA TERMINAL!!!
#elegir modelos
def configurar_modelo(cliente, modelo, mensajeDeEntrada):
    return cliente.chat.completions.create(
        model = modelo,
        messages = [{"role":"user", "content":mensajeDeEntrada}],
        stream = True #es importante cambiarlo a False al cerrar el host 
    )
        
#historial de mensajes
def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

#titulo de la ventana web
st.set_page_config(page_title="MyChatBot", page_icon="🎀")

#titulo de la pag
st.title("Mi conversación con MyChatBot")

#input de nombre
nombre = st.text_input("¿Cómo te llamás?")

#botón
if st.button("¡Hola, MyChatBot! :)"):
    if not nombre:
        st.write(f"¡Hola! Me alegra verte por acá.")
    else:
        st.write(f"¡Hola, {nombre}! Me alegra verte por acá.")
#fin botón

#funcion configurar pag
def configurar_pagina(): 
    st.title("¿En qué te puedo ayudar?")  #2do titulo
    st.sidebar.title("Configuración de MyChatBot:")
    opcion = st.sidebar.selectbox(
        "Elegí un modelo para MyChatBot", #titulo,
        options = MODELOS, #opciones
        index = 1
    )
    return opcion

def actualizar_historial(rol, contenido, avatar):
    st.session_state.mensajes.append({"role":rol, "content": contenido, "avatar": avatar})

def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar = mensaje ["avatar"]):
            st.markdown(mensaje["content"])

#espacio donde se visualizarán los mensajes
def area_chat():
    contenedorDelChat= st.container(height = 400, border = True)
    with contenedorDelChat:
        mostrar_historial()

def generar_respuesta(chat_completo):
    respuesta_completa = "" #variable vacia oomaigo
    for frase in chat_completo:
        if frase.choices[0].delta.content: #filtramos los datos NONE
            respuesta_completa += frase.choices[0].delta.content
            yield frase.choices[0].delta.content
    return respuesta_completa

#cuerpo de nuestro chatbot
def main():
    modelo = configurar_pagina()
    clienteUsuario = crear_usuario_groq()
    inicializar_estado()
    area_chat()

    mensaje = st.chat_input("Escribe tu mensaje...")
    if mensaje:
        actualizar_historial("user", mensaje, "✨") #se muestra el mensaje del usuario
        chat_completo = configurar_modelo(clienteUsuario, modelo, mensaje) #obtenemos la respuesta
        if chat_completo: #verificamos que la variable tenga contenido
            with st.chat_message("assistant"): 
                respuesta_completa = st.write_stream(generar_respuesta(chat_completo))
                actualizar_historial("assistant", respuesta_completa, "🔮")
                st.rerun() #va actualizando la pag
                print(mensaje)

if __name__ == "__main__":

    main()


