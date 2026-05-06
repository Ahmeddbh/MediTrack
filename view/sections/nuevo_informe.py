import streamlit as st
from pymongo import MongoClient
from scripts.db import get_collection
from scripts.openfda import consultar_openfda
from scripts.generar_informe import generar_informe_paciente
from datetime import datetime
import os

def render():
    st.title(" Nuevo Informe de Ingreso")
    st.caption("Rellena los datos del paciente. Al guardar se enriquecerá automáticamente con openFDA y se generará el informe PDF.")
    st.divider()

    with st.form("form_nuevo_informe"):
        st.subheader("Antecedentes / Motivo de consulta")
        antecedentes = st.text_area("Antecedentes / Motivo de consulta", label_visibility="collapsed")
        
        st.divider()
        
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Datos personales")
            name               = st.text_input("Nombre completo")
            age                = st.number_input("Edad", min_value=0, max_value=120, step=1)
            gender             = st.selectbox("Género", ["Male", "Female"])
            blood_type         = st.selectbox("Grupo sanguíneo", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
            insurance_provider = st.text_input("Aseguradora")
            billing_amount     = st.number_input("Importe facturado (USD)", min_value=0.0, step=0.01)
            room_number        = st.number_input("Número de habitación", min_value=1, step=1)

        with col2:
            st.subheader("Datos clínicos")
            medical_condition = st.text_input("Diagnóstico")
            admission_type    = st.selectbox("Tipo de admisión", ["Urgent", "Elective", "Emergency"])
            medication        = st.text_input("Medicación")
            dosage            = st.text_input("Dosis / Frecuencia (ej: 500mg cada 8 horas)")
            test_results      = st.selectbox("Resultado de pruebas", ["Normal", "Abnormal", "Inconclusive"])
            doctor            = st.text_input("Médico responsable")
            hospital          = st.text_input("Hospital")
            date_of_admission = st.date_input("Fecha de ingreso")
            time_of_admission = st.time_input("Hora de entrada")
            discharge_date    = st.date_input("Fecha de alta")
            time_of_discharge = st.time_input("Hora de salida")
        
        st.divider()
        
        st.subheader("Comentarios del médico")
        comentarios  = st.text_area("Comentarios del médico", label_visibility="collapsed")

        submitted = st.form_submit_button(" Guardar y generar informe", use_container_width=True)

    if submitted:
        if not name or not doctor or not hospital:
            st.error("Por favor rellena al menos el nombre, médico y hospital.")
            return

        if discharge_date < date_of_admission:
            st.error("La fecha de alta no puede ser anterior a la fecha de ingreso.")
            return

        col_db = get_collection()
        stay_days = (discharge_date - date_of_admission).days

        with st.spinner("Consultando openFDA..."):
            fda_info = consultar_openfda(medication)

        doc = {
            "name":               name,
            "age":                int(age),
            "gender":             gender,
            "blood_type":         blood_type,
            "medical_condition":  medical_condition,
            "date_of_admission":  datetime.combine(date_of_admission, time_of_admission),
            "discharge_date":     datetime.combine(discharge_date, time_of_discharge),
            "stay_days":          stay_days,
            "doctor":             doctor,
            "hospital":           hospital,
            "insurance_provider": insurance_provider,
            "billing_amount":     float(billing_amount),
            "room_number":        int(room_number),
            "admission_type":     admission_type,
            "medication":         medication,
            "dosage":             dosage,
            "test_results":       test_results,
            "fda_info":           fda_info,
            "antecedentes":       antecedentes if antecedentes else None,
            "comentarios":        comentarios if comentarios else None
        }

        resultado = col_db.insert_one(doc)
        doc["_id"] = resultado.inserted_id

        with st.spinner("Generando informe clínico con IA..."):
            texto_informe = generar_informe_paciente(doc)

        # Guardar PDF profesional
        from scripts.generar_pdf import generar_pdf_profesional
        
        nombre_archivo = f"informes/{name.replace(' ', '_')}_{date_of_admission.strftime('%Y%m%d')}.pdf"
        generar_pdf_profesional(nombre_archivo, doc, texto_informe)

        st.success(f"✅ Paciente **{name}** registrado y informe generado correctamente.")

        st.subheader("Informe generado")
        st.markdown(texto_informe)

        with open(nombre_archivo, "rb") as f:
            st.download_button(
                label="📥 Descargar informe PDF",
                data=f,
                file_name=os.path.basename(nombre_archivo),
                mime="application/pdf"
            )