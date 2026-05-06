import streamlit as st
import plotly.express as px
import pandas as pd
from scripts.db import get_collection
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def explicar_con_ia(datos, contexto):
    prompt = f"""
Eres un analista médico. En dos o tres frases en español, explica de forma clara y concisa 
lo que muestran estos datos estadísticos de un sistema hospitalario.
No inventes nada, basa tu respuesta únicamente en los datos proporcionados.

Contexto: {contexto}
Datos: {datos}
"""
    respuesta = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
        temperature=0.3
    )
    return respuesta.choices[0].message.content

def render():
    st.title("Estadísticas del Sistema")
    st.caption("Selecciona una consulta para visualizar los datos.")
    st.divider()

    col_db = get_collection()

    consulta = st.selectbox("Selecciona una consulta", [
        "Diagnósticos más frecuentes",
        "Medicamentos más prescritos",
        "Estancia media por diagnóstico",
        "Distribución por tipo de admisión",
        "Resultados de pruebas diagnósticas",
        "Pacientes por grupo sanguíneo",
        "Hospitales con más ingresos",
        "Médicos con más pacientes",
        "Distribución por género",
        "Importe medio facturado por diagnóstico",
    ])

    ejecutar = st.button("Consultar", use_container_width=True)

    if ejecutar:
        st.divider()

        # ── 1. DIAGNÓSTICOS MÁS FRECUENTES ──────────────
        if consulta == "Diagnósticos más frecuentes":
            data = list(col_db.aggregate([
                {"$group": {"_id": "$medical_condition", "total": {"$sum": 1}}},
                {"$sort": {"total": -1}}, {"$limit": 10}
            ]))
            df = pd.DataFrame(data).rename(columns={"_id": "Diagnóstico", "total": "Casos"})
            st.subheader("Diagnósticos más frecuentes")
            fig = px.bar(df, x="Diagnóstico", y="Casos",
                         color="Casos", color_continuous_scale="Greens")
            fig.update_layout(coloraxis_showscale=False)
            st.plotly_chart(fig, use_container_width=True)
            st.table(df)
            with st.spinner("Analizando con IA..."):
                st.info(explicar_con_ia(data, "diagnósticos más frecuentes en el sistema hospitalario"))

        # ── 2. MEDICAMENTOS MÁS PRESCRITOS ───────────────
        elif consulta == "Medicamentos más prescritos":
            data = list(col_db.aggregate([
                {"$group": {"_id": "$medication", "total": {"$sum": 1}}},
                {"$sort": {"total": -1}}, {"$limit": 10}
            ]))
            df = pd.DataFrame(data).rename(columns={"_id": "Medicamento", "total": "Prescripciones"})
            st.subheader("Medicamentos más prescritos")
            fig = px.bar(df, x="Medicamento", y="Prescripciones",
                         color="Prescripciones", color_continuous_scale="Greens")
            fig.update_layout(coloraxis_showscale=False)
            st.plotly_chart(fig, use_container_width=True)
            st.table(df)
            with st.spinner("Analizando con IA..."):
                st.info(explicar_con_ia(data, "medicamentos más prescritos en el sistema hospitalario"))

        # ── 3. ESTANCIA MEDIA POR DIAGNÓSTICO ────────────
        elif consulta == "Estancia media por diagnóstico":
            data = list(col_db.aggregate([
                {"$group": {"_id": "$medical_condition", "media": {"$avg": "$stay_days"}}},
                {"$sort": {"media": -1}}
            ]))
            df = pd.DataFrame(data).rename(columns={"_id": "Diagnóstico", "media": "Media días"})
            df["Media días"] = df["Media días"].round(1)
            st.subheader("Estancia media en días por diagnóstico")
            fig = px.bar(df, x="Diagnóstico", y="Media días",
                         color="Media días", color_continuous_scale="Greens")
            fig.update_layout(coloraxis_showscale=False)
            st.plotly_chart(fig, use_container_width=True)
            st.table(df)
            with st.spinner("Analizando con IA..."):
                st.info(explicar_con_ia(data, "estancia media en días por diagnóstico"))

        # ── 4. DISTRIBUCIÓN POR TIPO DE ADMISIÓN ─────────
        elif consulta == "Distribución por tipo de admisión":
            data = list(col_db.aggregate([
                {"$group": {"_id": "$admission_type", "total": {"$sum": 1}}}
            ]))
            df = pd.DataFrame(data).rename(columns={"_id": "Tipo", "total": "Total"})
            st.subheader("Distribución por tipo de admisión")
            fig = px.pie(df, names="Tipo", values="Total",
                         color_discrete_sequence=px.colors.sequential.Greens)
            st.plotly_chart(fig, use_container_width=True)
            st.table(df)
            with st.spinner("Analizando con IA..."):
                st.info(explicar_con_ia(data, "distribución de ingresos por tipo de admisión"))

        # ── 5. RESULTADOS DE PRUEBAS ──────────────────────
        elif consulta == "Resultados de pruebas diagnósticas":
            data = list(col_db.aggregate([
                {"$group": {"_id": "$test_results", "total": {"$sum": 1}}}
            ]))
            df = pd.DataFrame(data).rename(columns={"_id": "Resultado", "total": "Total"})
            st.subheader("Resultados de pruebas diagnósticas")
            fig = px.pie(df, names="Resultado", values="Total",
                         color_discrete_sequence=px.colors.sequential.Greens)
            st.plotly_chart(fig, use_container_width=True)
            st.table(df)
            with st.spinner("Analizando con IA..."):
                st.info(explicar_con_ia(data, "distribución de resultados de pruebas diagnósticas"))

        # ── 6. PACIENTES POR GRUPO SANGUÍNEO ─────────────
        elif consulta == "Pacientes por grupo sanguíneo":
            data = list(col_db.aggregate([
                {"$group": {"_id": "$blood_type", "total": {"$sum": 1}}},
                {"$sort": {"total": -1}}
            ]))
            df = pd.DataFrame(data).rename(columns={"_id": "Grupo sanguíneo", "total": "Pacientes"})
            st.subheader("Pacientes por grupo sanguíneo")
            fig = px.bar(df, x="Grupo sanguíneo", y="Pacientes",
                         color="Pacientes", color_continuous_scale="Greens")
            fig.update_layout(coloraxis_showscale=False)
            st.plotly_chart(fig, use_container_width=True)
            st.table(df)
            with st.spinner("Analizando con IA..."):
                st.info(explicar_con_ia(data, "distribución de pacientes por grupo sanguíneo"))

        # ── 7. HOSPITALES CON MÁS INGRESOS ───────────────
        elif consulta == "Hospitales con más ingresos":
            data = list(col_db.aggregate([
                {"$group": {"_id": "$hospital", "total": {"$sum": 1}}},
                {"$sort": {"total": -1}}, {"$limit": 10}
            ]))
            df = pd.DataFrame(data).rename(columns={"_id": "Hospital", "total": "Ingresos"})
            st.subheader("Hospitales con más ingresos")
            fig = px.bar(df, x="Hospital", y="Ingresos",
                         color="Ingresos", color_continuous_scale="Greens")
            fig.update_layout(coloraxis_showscale=False)
            st.plotly_chart(fig, use_container_width=True)
            st.table(df)
            with st.spinner("Analizando con IA..."):
                st.info(explicar_con_ia(data, "hospitales con mayor número de ingresos"))

        # ── 8. MÉDICOS CON MÁS PACIENTES ─────────────────
        elif consulta == "Médicos con más pacientes":
            data = list(col_db.aggregate([
                {"$group": {"_id": "$doctor", "total": {"$sum": 1}}},
                {"$sort": {"total": -1}}, {"$limit": 10}
            ]))
            df = pd.DataFrame(data).rename(columns={"_id": "Médico", "total": "Pacientes"})
            st.subheader("Médicos con más pacientes")
            fig = px.bar(df, x="Médico", y="Pacientes",
                         color="Pacientes", color_continuous_scale="Greens")
            fig.update_layout(coloraxis_showscale=False)
            st.plotly_chart(fig, use_container_width=True)
            st.table(df)
            with st.spinner("Analizando con IA..."):
                st.info(explicar_con_ia(data, "médicos con mayor número de pacientes atendidos"))

        # ── 9. DISTRIBUCIÓN POR GÉNERO ────────────────────
        elif consulta == "Distribución por género":
            data = list(col_db.aggregate([
                {"$group": {"_id": "$gender", "total": {"$sum": 1}}}
            ]))
            df = pd.DataFrame(data).rename(columns={"_id": "Género", "total": "Total"})
            st.subheader("Distribución por género")
            fig = px.pie(df, names="Género", values="Total",
                         color_discrete_sequence=px.colors.sequential.Greens)
            st.plotly_chart(fig, use_container_width=True)
            st.table(df)
            with st.spinner("Analizando con IA..."):
                st.info(explicar_con_ia(data, "distribución de pacientes por género"))

        # ── 10. IMPORTE MEDIO POR DIAGNÓSTICO ────────────
        elif consulta == "Importe medio facturado por diagnóstico":
            data = list(col_db.aggregate([
                {"$group": {"_id": "$medical_condition",
                            "importe_medio": {"$avg": "$billing_amount"}}},
                {"$sort": {"importe_medio": -1}}
            ]))
            df = pd.DataFrame(data).rename(
                columns={"_id": "Diagnóstico", "importe_medio": "Importe medio (USD)"})
            df["Importe medio (USD)"] = df["Importe medio (USD)"].round(2)
            st.subheader("Importe medio facturado por diagnóstico")
            fig = px.bar(df, x="Diagnóstico", y="Importe medio (USD)",
                         color="Importe medio (USD)", color_continuous_scale="Greens")
            fig.update_layout(coloraxis_showscale=False)
            st.plotly_chart(fig, use_container_width=True)
            st.table(df)
            with st.spinner("Analizando con IA..."):
                st.info(explicar_con_ia(data, "importe medio facturado por diagnóstico"))