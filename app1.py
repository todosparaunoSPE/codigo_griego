# -*- coding: utf-8 -*-
"""
Created on Mon May 12 18:02:17 2025

@author: jahop
"""

import streamlit as st
import urllib.parse
import pyperclip

# Estilo de fondo
page_bg_img = """
<style>
[data-testid="stAppViewContainer"]{
background:
radial-gradient(black 15%, transparent 16%) 0 0,
radial-gradient(black 15%, transparent 16%) 8px 8px,
radial-gradient(rgba(255,255,255,.1) 15%, transparent 20%) 0 1px,
radial-gradient(rgba(255,255,255,.1) 15%, transparent 20%) 8px 9px;
background-color:#282828;
background-size:16px 16px;
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)


# Mapeo de letras griegas a español
griego_a_espanol = {
    'α': 'a', 'β': 'b', 'γ': 'g', 'δ': 'd', 'ε': 'e',
    'ζ': 'z', 'η': 'h', 'θ': 'th', 'ι': 'i', 'κ': 'k',
    'λ': 'l', 'μ': 'm', 'ν': 'n', 'ξ': 'x', 'ο': 'o',
    'π': 'p', 'ρ': 'r', 'σ': 's', 'ς': 's', 'τ': 't',
    'υ': 'y', 'φ': 'ph', 'χ': 'ch', 'ψ': 'ps', 'ω': 'w',
    'Α': 'A', 'Β': 'B', 'Γ': 'G', 'Δ': 'D', 'Ε': 'E',
    'Ζ': 'Z', 'Η': 'H', 'Θ': 'Th', 'Ι': 'I', 'Κ': 'K',
    'Λ': 'L', 'Μ': 'M', 'Ν': 'N', 'Ξ': 'X', 'Ο': 'O',
    'Π': 'P', 'Ρ': 'R', 'Σ': 'S', 'Τ': 'T', 'Υ': 'Y',
    'Φ': 'Ph', 'Χ': 'Ch', 'Ψ': 'Ps', 'Ω': 'W'
}

# Mapeo inverso (español a griego)
espanol_a_griego = {v: k for k, v in griego_a_espanol.items()}

def traducir_griego_a_espanol(texto):
    resultado = []
    i = 0
    n = len(texto)
    while i < n:
        for length in [2, 1]:
            if i + length <= n:
                substring = texto[i:i+length]
                if substring in griego_a_espanol:
                    resultado.append(griego_a_espanol[substring])
                    i += length
                    break
        else:
            resultado.append(texto[i])
            i += 1
    return ''.join(resultado)

def traducir_espanol_a_griego(texto):
    resultado = []
    i = 0
    n = len(texto)
    while i < n:
        for length in [2, 1]:
            if i + length <= n:
                substring = texto[i:i+length].lower()
                if substring in espanol_a_griego:
                    if texto[i:i+length].istitle():
                        traducido = espanol_a_griego[substring].title()
                    elif texto[i:i+length].isupper():
                        traducido = espanol_a_griego[substring].upper()
                    else:
                        traducido = espanol_a_griego[substring]
                    resultado.append(traducido)
                    i += length
                    break
        else:
            resultado.append(texto[i])
            i += 1
    return ''.join(resultado)

def crear_enlace_whatsapp(texto, texto_a_copiar):
    pyperclip.copy(texto_a_copiar)
    st.session_state.copied = True
    texto_codificado = urllib.parse.quote(texto)
    return f"https://wa.me/?text={texto_codificado}"

# Configuración del sidebar
with st.sidebar:
    st.title("Información")
    st.markdown("---")
    st.markdown("### Creado por:")
    st.markdown("**Javier Horacio Pérez Ricárdez**")
    st.markdown("---")
    st.markdown("### Alfabeto Griego:")
    st.write("""
    - **Minúsculas**: α β γ δ ε ζ η θ ι κ λ μ ν ξ ο π ρ σ/ς τ υ φ χ ψ ω
    - **Mayúsculas**: Α Β Γ Δ Ε Ζ Η Θ Ι Κ Λ Μ Ν Ξ Ο Π Ρ Σ Τ Υ Φ Χ Ψ Ω
    """)
    st.markdown("---")
    st.markdown("### Instrucciones:")
    st.write("""
    1. Selecciona la operación deseada
    2. Introduce tu texto
    3. Haz clic en el botón correspondiente
    4. Usa el botón de WhatsApp para compartir
    """)

# Configuración de la aplicación principal
st.title("🔠 Generador y Traductor de Código Griego")

# Inicializar estado para feedback de copiado
if 'copied' not in st.session_state:
    st.session_state.copied = False

opcion = st.radio("Selecciona una opción:", 
                 ("Generar código griego", "Traducir código griego a español"),
                 horizontal=True)

if opcion == "Generar código griego":
    texto_original = st.text_area("Introduce el texto en español para convertir a griego:", 
                                height=150, 
                                placeholder="Escribe aquí tu texto en español...")
    if st.button("Generar Código Griego", type="primary"):
        if texto_original:
            texto_griego = traducir_espanol_a_griego(texto_original)
            st.subheader("Resultado:")
            st.code(texto_griego, language=None)
            
            st.session_state.texto_compartir = f"Código Griego generado:\n{texto_griego}"
            st.session_state.texto_a_copiar = texto_griego
            st.session_state.copied = False
        else:
            st.warning("Por favor introduce un texto para generar el código griego.")
else:
    texto_griego = st.text_area("Introduce el código en griego para traducir a español:", 
                              height=150, 
                              placeholder="Escribe aquí tu texto en griego...")
    if st.button("Traducir a Español", type="primary"):
        if texto_griego:
            texto_traducido = traducir_griego_a_espanol(texto_griego)
            st.subheader("Resultado:")
            st.code(texto_traducido, language=None)
            
            st.session_state.texto_compartir = f"Traducción del griego:\nOriginal: {texto_griego}\nTraducción: {texto_traducido}"
            st.session_state.texto_a_copiar = texto_traducido
            st.session_state.copied = False
        else:
            st.warning("Por favor introduce un código en griego para traducir.")

# Mostrar botón de WhatsApp si hay texto para compartir
if 'texto_compartir' in st.session_state and st.session_state.texto_compartir:
    enlace_whatsapp = crear_enlace_whatsapp(
        st.session_state.texto_compartir,
        st.session_state.texto_a_copiar
    )
    
    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown(f"""
        <a href="{enlace_whatsapp}" target="_blank">
            <button style="background-color:#25D366;color:white;border-radius:5px;padding:10px 20px;width:100%">
                {'✓ Copiado! WhatsApp' if st.session_state.copied else '📋 WhatsApp'}
            </button>
        </a>
        """, unsafe_allow_html=True)
    
    with col2:
        if st.session_state.copied:
            st.success("Texto copiado al portapapeles. Ábre WhatsApp y pégalo (Ctrl+V)")

# Pie de página
st.markdown("---")
st.caption("Aplicación creada por Javier Horacio Pérez Ricárdez - Generador y traductor de código griego")
