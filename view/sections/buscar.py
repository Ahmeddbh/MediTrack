import streamlit as st
from scripts.db import get_collection
from scripts.generar_informe import generar_informe_paciente
from scripts.generar_pdf import generar_pdf_profesional
from datetime import datetime
import os

def render():
    st.title("Buscar y Filtrar Pacientes")
    st.caption("Filtra los pacientes por cualquier combinación de campos.")
    st.divider()

    col_db = get_collection()

    # ── INICIALIZAR SESSION STATE ────────────────────────
    if 'pagina_actual' not in st.session_state:
        st.session_state.pagina_actual = 0
    if 'query_almacenada' not in st.session_state:
        st.session_state.query_almacenada = None
    if 'total_resultados' not in st.session_state:
        st.session_state.total_resultados = 0

    # ── FILTROS ──────────────────────────────────────────
    with st.expander("Filtros", expanded=True):
        col1, col2, col3 = st.columns(3)

        with col1:
            nombre     = st.text_input("Nombre del paciente")
            doctor     = st.text_input("Médico")
            hospital   = st.text_input("Hospital")

        with col2:
            genero     = st.selectbox("Género", ["Todos", "Male", "Female"])
            grupo_sang = st.selectbox("Grupo sanguíneo", ["Todos", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
            diagnostico= st.text_input("Diagnóstico")

        with col3:
            admision   = st.selectbox("Tipo de admisión", ["Todos", "Urgent", "Elective", "Emergency"])
            fecha_desde= st.date_input("Fecha de ingreso desde", value=None)
            fecha_hasta= st.date_input("Fecha de ingreso hasta", value=None)

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        buscar = st.button("Buscar", use_container_width=True)
    with col_btn2:
        limpiar = st.button("Limpiar filtros", use_container_width=True)

    if limpiar:
        st.session_state.pagina_actual = 0
        st.session_state.query_almacenada = None
        st.rerun()

    if buscar:
        st.session_state.pagina_actual = 0
        
        # ── CONSTRUIR QUERY ──────────────────────────────
        query = {}

        if nombre:
            query["name"] = {"$regex": nombre, "$options": "i"}
        if doctor:
            query["doctor"] = {"$regex": doctor, "$options": "i"}
        if hospital:
            query["hospital"] = {"$regex": hospital, "$options": "i"}
        if diagnostico:
            query["medical_condition"] = {"$regex": diagnostico, "$options": "i"}
        if genero != "Todos":
            query["gender"] = genero
        if grupo_sang != "Todos":
            query["blood_type"] = grupo_sang
        if admision != "Todos":
            query["admission_type"] = admision
        if fecha_desde and fecha_hasta:
            query["date_of_admission"] = {
                "$gte": datetime.combine(fecha_desde, datetime.min.time()),
                "$lte": datetime.combine(fecha_hasta, datetime.max.time())
            }

        st.session_state.query_almacenada = query
        st.session_state.total_resultados = col_db.count_documents(query)

    # ── MOSTRAR RESULTADOS ───────────────────────────
    if st.session_state.query_almacenada is not None:
        if st.session_state.total_resultados == 0:
            st.warning("No se encontraron pacientes con esos filtros.")
            return

        st.success(f"Se encontraron **{st.session_state.total_resultados}** pacientes")
        st.divider()

        # ── PAGINACIÓN ───────────────────────────────
        items_por_pagina = 20
        inicio = st.session_state.pagina_actual * items_por_pagina
        fin = inicio + items_por_pagina

        resultados = list(col_db.find(st.session_state.query_almacenada).skip(inicio).limit(items_por_pagina))

        # Mostrar resultados de esta página
        for doc in resultados:
            with st.expander(f"{doc.get('name')} — {doc.get('medical_condition')} — {doc.get('date_of_admission').strftime('%d/%m/%Y') if doc.get('date_of_admission') else 'Sin fecha'}"):
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown(f"**Edad:** {doc.get('age')} años")
                    st.markdown(f"**Género:** {doc.get('gender')}")
                    st.markdown(f"**Grupo sanguíneo:** {doc.get('blood_type')}")
                    st.markdown(f"**Diagnóstico:** {doc.get('medical_condition')}")
                    st.markdown(f"**Tipo de admisión:** {doc.get('admission_type')}")
                    st.markdown(f"**Días de estancia:** {doc.get('stay_days')}")

                with col2:
                    st.markdown(f"**Médico:** {doc.get('doctor')}")
                    st.markdown(f"**Hospital:** {doc.get('hospital')}")
                    st.markdown(f"**Medicación:** {doc.get('medication')}")
                    st.markdown(f"**Dosis:** {doc.get('dosage', 'No especificada')}")
                    st.markdown(f"**Resultado pruebas:** {doc.get('test_results')}")
                    st.markdown(f"**Aseguradora:** {doc.get('insurance_provider')}")
                    st.markdown(f"**Importe:** ${doc.get('billing_amount', 0):.2f}")

                if doc.get('antecedentes'):
                    st.markdown(f"**Antecedentes:** {doc.get('antecedentes')}")
                if doc.get('comentarios'):
                    st.markdown(f"**Comentarios médico:** {doc.get('comentarios')}")

                # Botón generar informe PDF
                if st.button(f"Generar informe PDF", key=f"btn_{doc['_id']}"):
                    with st.spinner("Generando informe con IA..."):
                        texto = generar_informe_paciente(doc)

                    nombre_archivo = f"informes/{doc.get('name', 'paciente').replace(' ', '_')}_{doc.get('date_of_admission').strftime('%Y%m%d') if doc.get('date_of_admission') else 'sin_fecha'}.pdf"
                    
                    try:
                        generar_pdf_profesional(nombre_archivo, doc, texto)
                        st.success("Informe generado correctamente.")
                        
                        with open(nombre_archivo, "rb") as f:
                            st.download_button(
                                label="Descargar PDF",
                                data=f,
                                file_name=os.path.basename(nombre_archivo),
                                mime="application/pdf",
                                key=f"dl_{doc['_id']}"
                            )
                    except Exception as e:
                        st.error(f"Error al generar el PDF: {str(e)}")

        st.divider()

        # ── CONTROLES DE PAGINACIÓN ──────────────────────
        col_prev, col_info, col_next = st.columns([1, 2, 1])

        total_paginas = (st.session_state.total_resultados + items_por_pagina - 1) // items_por_pagina

        with col_info:
            st.write(f"**Página {st.session_state.pagina_actual + 1} de {total_paginas}** | "
                    f"Mostrando {min(fin, st.session_state.total_resultados)} de {st.session_state.total_resultados} resultados")

        col_prev, col_next = st.columns(2)
        
        with col_prev:
            if st.session_state.pagina_actual > 0:
                if st.button("Página anterior", use_container_width=True):
                    st.session_state.pagina_actual -= 1
                    st.rerun()

        with col_next:
            if st.session_state.pagina_actual < total_paginas - 1:
                if st.button("Página siguiente", use_container_width=True):
                    st.session_state.pagina_actual += 1
                    st.rerun()