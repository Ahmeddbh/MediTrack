import streamlit as st
from scripts.db import get_collection
from scripts.generar_informe import generar_informe_paciente
from scripts.generar_pdf import generar_pdf_profesional
from datetime import datetime
import os

def render():
    st.title("Pacientes del Día")
    st.caption("Consulta los ingresos y altas registrados en una fecha concreta.")
    st.divider()

    col_db = get_collection()

    fecha = st.date_input("Selecciona una fecha", value=datetime.today())

    col1, col2 = st.columns(2)
    with col1:
        ver_ingresos = st.button("Ver ingresos", use_container_width=True)
    with col2:
        ver_altas = st.button("Ver altas", use_container_width=True)

    def mostrar_pacientes(docs, etiqueta_fecha):
        if not docs:
            st.warning(f"No hay pacientes con {etiqueta_fecha} en esa fecha.")
            return

        st.success(f"Se encontraron **{len(docs)}** paciente(s).")
        st.divider()

        for doc in docs:
            fecha_ingreso = doc.get("date_of_admission")
            fecha_alta = doc.get("discharge_date")

            with st.expander(f"{doc.get('name')} — {doc.get('medical_condition')}"):
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
                    st.markdown(f"**Resultado pruebas:** {doc.get('test_results')}")
                    st.markdown(f"**Aseguradora:** {doc.get('insurance_provider')}")
                    st.markdown(f"**Importe:** ${doc.get('billing_amount', 0):.2f}")

                if fecha_ingreso:
                    st.markdown(f"**Fecha de ingreso:** {fecha_ingreso.strftime('%d/%m/%Y %H:%M') if isinstance(fecha_ingreso, datetime) else fecha_ingreso}")
                if fecha_alta:
                    st.markdown(f"**Fecha de alta:** {fecha_alta.strftime('%d/%m/%Y %H:%M') if isinstance(fecha_alta, datetime) else fecha_alta}")

                if doc.get("antecedentes"):
                    st.markdown(f"**Antecedentes:** {doc.get('antecedentes')}")
                if doc.get("comentarios"):
                    st.markdown(f"**Comentarios médico:** {doc.get('comentarios')}")

                if st.button("Generar informe PDF", key=str(doc["_id"])):
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

    if ver_ingresos:
        st.subheader(f"Ingresos del {fecha.strftime('%d/%m/%Y')}")
        inicio = datetime.combine(fecha, datetime.min.time())
        fin = datetime.combine(fecha, datetime.max.time())
        docs = list(col_db.find({
            "date_of_admission": {"$gte": inicio, "$lte": fin}
        }))
        mostrar_pacientes(docs, "fecha de ingreso")

    if ver_altas:
        st.subheader(f"Altas del {fecha.strftime('%d/%m/%Y')}")
        inicio = datetime.combine(fecha, datetime.min.time())
        fin = datetime.combine(fecha, datetime.max.time())
        docs = list(col_db.find({
            "discharge_date": {"$gte": inicio, "$lte": fin}
        }))
        mostrar_pacientes(docs, "fecha de alta")