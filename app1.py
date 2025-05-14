# -*- coding: utf-8 -*-
"""
Created on Mon May 12 18:02:17 2025

@author: jahop
"""

import streamlit as st
import urllib.parse

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

def crear_mensaje_whatsapp(texto_principal, es_griego=True):
    enlace_app = "https://codigogriego-fgp3p4mlihddwqvxb3ptry.streamlit.app/"
    
    if es_griego:
        instruccion = f"\n\n🔁 ¿Quieres traducir este código griego a español? Visita: {enlace_app}"
    else:
        instruccion = f"\n\n🔁 ¿Quieres convertir texto español a griego? Visita: {enlace_app}"
    
    return texto_principal + instruccion

# Inicialización del estado de sesión
if 'texto_compartir' not in st.session_state:
    st.session_state.texto_compartir = ""
if 'texto_a_copiar' not in st.session_state:
    st.session_state.texto_a_copiar = ""
if 'es_griego' not in st.session_state:
    st.session_state.es_griego = False

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
    st.markdown("### Compartir esta app:")
    mensaje_app = crear_mensaje_whatsapp("¡Descubre esta increíble app para traducir código griego!", False)
    st.markdown(f"""
    <a href="https://wa.me/?text={urllib.parse.quote(mensaje_app)}" target="_blank">
        <button style="background-color:#25D366;color:white;border-radius:5px;padding:10px 20px;width:100%">
            📤 Compartir App en WhatsApp
        </button>
    </a>
    """, unsafe_allow_html=True)

# Configuración de la aplicación principal
st.title("🔠 Generador y Traductor de Código Griego")

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
            
            st.session_state.texto_compartir = texto_griego
            st.session_state.texto_a_copiar = texto_griego
            st.session_state.es_griego = True
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
            
            st.session_state.texto_compartir = texto_traducido
            st.session_state.texto_a_copiar = texto_traducido
            st.session_state.es_griego = False
        else:
            st.warning("Por favor introduce un código en griego para traducir.")

# Mostrar botones de acción
if st.session_state.texto_compartir:
    col1, col2 = st.columns(2)
    
    with col1:
        # Botón de WhatsApp con enlace de retorno
        mensaje_whatsapp = crear_mensaje_whatsapp(
            st.session_state.texto_compartir,
            st.session_state.es_griego
        )
        enlace_whatsapp = f"https://wa.me/?text={urllib.parse.quote(mensaje_whatsapp)}"
        st.markdown(f"""
        <a href="{enlace_whatsapp}" target="_blank">
            <button style="background-color:#25D366;color:white;border-radius:5px;padding:10px 20px;width:100%">
                📤 Compartir en WhatsApp
            </button>
        </a>
        """, unsafe_allow_html=True)
    
    with col2:
        # Alternativa para copiar el texto
        st.code(st.session_state.texto_a_copiar, language=None)
        if st.button("📋 Seleccionar texto para copiar", use_container_width=True):
            st.success("Texto seleccionado. Usa Ctrl+C para copiarlo")

# Pie de página
st.markdown("---")
st.caption("Aplicación creada por Javier Horacio Pérez Ricárdez - Generador y traductor de código griego")
