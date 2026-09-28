import streamlit as st


def mostrar_login():
    st.title("Iniciar Sesión")
    st.markdown("Por favor, ingresa tus credenciales para acceder al sistema.")

    with st.form("login_form"):
        usuario = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")
        submit = st.form_submit_button("Entrar")

        if submit:
            if "usuarios" in st.secrets:
                diccionario_usuarios = st.secrets["usuarios"]
                if (
                    usuario in diccionario_usuarios
                    and password == diccionario_usuarios[usuario]
                ):
                    st.session_state["logeado"] = True
                    st.session_state["usuario_actual"] = usuario
                    st.success(f"¡Bienvenido, {usuario}!")
                    st.rerun()
                else:
                    st.error("Usuario o contraseña incorrectos.")
            else:
                st.error(
                    "⚠️ No se encontró la configuración de usuarios"
                    " ('secrets.toml'). Por favor configúrala."
                )
