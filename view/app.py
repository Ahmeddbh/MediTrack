import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st

st.set_page_config(
    page_title="MediTrack",
    page_icon="🏥",
    layout="wide"
)

# ── ESTILOS PERSONALIZADOS ────────────────────────────────
st.markdown("""
    <style>
    .sidebar-title {
        font-size: 24px;
        font-weight: 700;
        color: #1f77b4;
    }
    .sidebar-subtitle {
        font-size: 12px;
        color: #666;
        margin-top: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# ── BARRA LATERAL ─────────────────────────────────────────
with st.sidebar:
    st.markdown('<p class="sidebar-title">MediTrack</p>', unsafe_allow_html=True)
    st.markdown('<p class="sidebar-subtitle">Sistema de Gestión Hospitalaria</p>', unsafe_allow_html=True)
    st.divider()
    
    seccion = st.radio(
        "Navegación",
        ["Nuevo Informe",
         "Buscar y Filtrar",
         "Informes Guardados",
         "Estadísticas",
         "Pacientes del Día"],
        label_visibility="collapsed"
    )
    
    st.divider()
    st.caption("Bases de Datos Avanzadas — 2025/2026")
    st.caption("Anas El Ouahabi | Ahmed Berday")

# ── SECCIONES ─────────────────────────────────────────────
if seccion == "Nuevo Informe":
    from view.sections.nuevo_informe import render
    render()

elif seccion == "Buscar y Filtrar":
    from view.sections.buscar import render
    render()

elif seccion == "Informes Guardados":
    from view.sections.informes_guardados import render
    render()

elif seccion == "Estadísticas":
    from view.sections.estadisticas import render
    render()

elif seccion == "Pacientes del Día":
    from view.sections.pacientes_dia import render
    render()