from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generar_informe_paciente(doc):
    fda = doc.get("fda_info") or {}

    prompt = f"""
Eres un médico especialista en farmacología redactando un informe clínico formal en español.
Basándote ÚNICAMENTE en los siguientes datos del paciente, redacta un informe clínico estructurado y detallado.
No inventes ningún dato que no esté aquí.

IMPORTANTE: Dedica especial atención a la sección de medicación y farmacología, analizando:
- Cómo la medicación se adapta al diagnóstico específico
- La relación entre los resultados de pruebas y la medicación prescrita
- Las posibles reacciones adversas según el perfil del paciente
- La dosificación apropiada según los días de estancia

DATOS DEL PACIENTE:
- Nombre: {doc.get('name')}
- Edad: {doc.get('age')} años
- Género: {doc.get('gender')}
- Grupo sanguíneo: {doc.get('blood_type')}
- Diagnóstico: {doc.get('medical_condition')}
- Tipo de ingreso: {doc.get('admission_type')}
- Fecha y hora de ingreso: {doc.get('date_of_admission')}
- Fecha y hora de alta: {doc.get('discharge_date')}
- Días de estancia: {doc.get('stay_days')}
- Médico responsable: {doc.get('doctor')}
- Hospital: {doc.get('hospital')}
- Medicación prescrita: {doc.get('medication')}
- Dosis / Frecuencia: {doc.get('dosage', 'No especificada')}
- Resultado de pruebas: {doc.get('test_results')}
- Importe facturado: {doc.get('billing_amount'):.2f} USD
- Antecedentes / Motivo de consulta: {doc.get('antecedentes') or 'No registrado'}
- Comentarios del médico: {doc.get('comentarios') or 'No registrado'}

INFORMACIÓN FARMACOLÓGICA DETALLADA DE openFDA PARA {doc.get('medication')}:

Medicamento: {doc.get('medication')}
- Nombre comercial: {fda.get('brand_name', 'No disponible')}
- Nombre genérico: {fda.get('generic_name', 'No disponible')}

INDICACIONES CLÍNICAS (FDA):
{fda.get('indications', 'No disponible')}

REACCIONES ADVERSAS REPORTADAS (FDA):
{fda.get('adverse_reactions', 'No disponible')}

ADVERTENCIAS Y CONTRAINDICACIONES (FDA):
{fda.get('warnings', 'No disponible')}

DOSIFICACIÓN Y ADMINISTRACIÓN (FDA):
{fda.get('dosage', 'No disponible')}

CONTEXTO DEL PACIENTE ACTUAL:
- Diagnóstico: {doc.get('medical_condition')}
- Tipo de ingreso: {doc.get('admission_type')}
- Resultado de pruebas: {doc.get('test_results')}
- Días de estancia: {doc.get('stay_days')}
- Grupo sanguíneo: {doc.get('blood_type')}
- Edad: {doc.get('age')} años
- Género: {doc.get('gender')}

ANÁLISIS FARMACOLÓGICO PERSONALIZADO:
Basándote en la información de FDA proporcionada y el contexto clínico del paciente:
- Evalúa si las indicaciones de FDA coinciden con el diagnóstico del paciente
- Analiza las reacciones adversas más probables según el perfil demográfico
- Relaciona las advertencias de FDA con los resultados de pruebas del paciente
- Proporciona recomendaciones de monitoreo específicas
- Indica si hay contraindicaciones potenciales según el grupo sanguíneo o edad

El informe debe tener estas secciones en español:
1. Datos del paciente y contexto clínico
2. Resumen del ingreso y evolución
3. Análisis farmacológico basado en datos reales de FDA
4. Relación indicación-diagnóstico y reacciones adversas esperadas
5. Recomendaciones de monitoreo y gestión de efectos secundarios
6. Conclusión y plan de seguimiento
"""

    respuesta = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1500,
        temperature=0.3
    )

    return respuesta.choices[0].message.content