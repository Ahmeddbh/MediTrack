from groq import Groq
from dotenv import load_dotenv
import os
import requests

load_dotenv()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def traducir_medicamento(nombre):
    respuesta = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{
            "role": "user",
            "content": f"Traduce al inglés el nombre de este medicamento: '{nombre}'. "
                       f"Responde ÚNICAMENTE con el nombre en inglés, sin explicaciones, "
                       f"sin puntos, sin nada más."
        }],
        max_tokens=20,
        temperature=0
    )
    return respuesta.choices[0].message.content.strip()

def consultar_openfda(medicamento):
    nombre_en = traducir_medicamento(medicamento)

    url = f"https://api.fda.gov/drug/label.json?search=openfda.brand_name:{nombre_en}&limit=1"
    r = requests.get(url)

    if r.status_code != 200:
        url = f"https://api.fda.gov/drug/label.json?search=openfda.generic_name:{nombre_en}&limit=1"
        r = requests.get(url)

    if r.status_code != 200:
        return None

    data = r.json()
    resultado = data["results"][0]

    return {
        "brand_name":        resultado.get("openfda", {}).get("brand_name", [None])[0],
        "generic_name":      resultado.get("openfda", {}).get("generic_name", [None])[0],
        "indications":       resultado.get("indications_and_usage", [None])[0],
        "warnings":          resultado.get("warnings", [None])[0],
        "adverse_reactions": resultado.get("adverse_reactions", [None])[0],
        "dosage":            resultado.get("dosage_and_administration", [None])[0],
    }
