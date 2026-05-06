import streamlit as st
import os
from datetime import datetime

def render():
    st.title("Informes Guardados")
    st.caption("Todos los informes PDF generados por el sistema.")
    st.divider()

    carpeta = "informes"

    if not os.path.exists(carpeta):
        st.warning("La carpeta de informes no existe todavía.")
        return

    archivos = [f for f in os.listdir(carpeta) if f.endswith(".pdf")]

    if not archivos:
        st.info("No hay informes generados todavía.")
        return

    # ── INICIALIZAR SESSION STATE ────────────────────────
    if 'pagina_informes' not in st.session_state:
        st.session_state.pagina_informes = 0
    if 'filtros_informes' not in st.session_state:
        st.session_state.filtros_informes = None

    # ── FILTROS ──────────────────────────────────────────
    col1, col2 = st.columns(2)
    with col1:
        buscar_nombre = st.text_input("Buscar por nombre de paciente")
    with col2:
        fecha_filtro = st.date_input("Filtrar por fecha", value=None)

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        filtrar = st.button("Filtrar", use_container_width=True)
    with col_btn2:
        limpiar = st.button("Limpiar filtros", use_container_width=True)

    if limpiar:
        st.session_state.pagina_informes = 0
        st.session_state.filtros_informes = None
        st.rerun()

    if filtrar:
        st.session_state.pagina_informes = 0
        # Aplicar filtros
        if buscar_nombre or fecha_filtro:
            archivos_filtrados = archivos.copy()
            if buscar_nombre:
                archivos_filtrados = [f for f in archivos_filtrados if buscar_nombre.lower() in f.lower()]
            if fecha_filtro:
                fecha_str = fecha_filtro.strftime("%Y%m%d")
                archivos_filtrados = [f for f in archivos_filtrados if fecha_str in f]
            st.session_state.filtros_informes = archivos_filtrados
        else:
            st.session_state.filtros_informes = archivos

    # Usar filtros almacenados o todos los archivos
    archivos_mostrados = st.session_state.filtros_informes if st.session_state.filtros_informes is not None else archivos
    archivos_mostrados = sorted(archivos_mostrados, reverse=True)

    st.success(f"**{len(archivos_mostrados)}** informe(s) encontrado(s).")
    st.divider()

    # ── PAGINACIÓN ───────────────────────────────────────
    items_por_pagina = 10
    inicio = st.session_state.pagina_informes * items_por_pagina
    fin = inicio + items_por_pagina

    # ── LISTA DE INFORMES ────────────────────────────────
    for archivo in archivos_mostrados[inicio:fin]:
        ruta = os.path.join(carpeta, archivo)
        nombre_limpio = archivo.replace("_", " ").replace(".pdf", "")

        # Extraer fecha del nombre del archivo
        partes = archivo.replace(".pdf", "").split("_")
        fecha_legible = ""
        for parte in partes:
            if len(parte) == 8 and parte.isdigit():
                try:
                    fecha_legible = datetime.strptime(parte, "%Y%m%d").strftime("%d/%m/%Y")
                except:
                    pass

        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"**{nombre_limpio}** {f'— {fecha_legible}' if fecha_legible else ''}")
        with col2:
            with open(ruta, "rb") as f:
                st.download_button(
                    label="Descargar",
                    data=f,
                    file_name=archivo,
                    mime="application/pdf",
                    key=f"dl_{archivo}"
                )
        st.divider()

    # ── CONTROLES DE PAGINACIÓN ──────────────────────────
    if len(archivos_mostrados) > items_por_pagina:
        st.divider()
        col_prev, col_info, col_next = st.columns([1, 2, 1])

        total_paginas = (len(archivos_mostrados) + items_por_pagina - 1) // items_por_pagina

        with col_info:
            st.write(f"**Página {st.session_state.pagina_informes + 1} de {total_paginas}** | "
                    f"Mostrando {min(fin, len(archivos_mostrados))} de {len(archivos_mostrados)} resultados")

        col_prev, col_next = st.columns(2)
        
        with col_prev:
            if st.session_state.pagina_informes > 0:
                if st.button("Página anterior", use_container_width=True):
                    st.session_state.pagina_informes -= 1
                    st.rerun()

        with col_next:
            if st.session_state.pagina_informes < total_paginas - 1:
                if st.button("Página siguiente", use_container_width=True):
                    st.session_state.pagina_informes += 1
                    st.rerun()